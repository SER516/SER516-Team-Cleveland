from datetime import datetime, timedelta, timezone, date
from milestone.get_milestone import get_milestone
from concurrent.futures import ThreadPoolExecutor
from tasks.get_tasks import get_tasks_by_story_id
from userStory.getBusinessValue import get_business_value


def get_multi_sprint_data(milestone_ids, attribute_key, auth_token):
    sprint_burndown = {}
    for milestone_id in milestone_ids:
        burndown_data = get_burndown_chart_metric_detail(
            milestone_id,
            attribute_key,
            auth_token
        )
        sprint_burndown[burndown_data["sprint"]] = {
            "combined_burndown": burndown_data["combined_burndown"],
            "sprint": burndown_data["sprint"],
            "total_sp": burndown_data["total_sp"],
            "total_bv": burndown_data["total_bv"]
        }

    return sprint_burndown



def get_burndown_chart_metric_detail(milestone_id, attribute_key, auth_token):
    milestone = get_milestone(milestone_id, auth_token)

    partial_burndown, bv_burndown, total_burndown, combined_burndown = \
        calc_burndown_day_data(
            auth_token, milestone, attribute_key
        )
    partial_burndown = list(partial_burndown.values())
    partial_burndown.sort(key=lambda item: item["date"])
    bv_burndown = list(bv_burndown.values())
    bv_burndown.sort(key=lambda item: item["date"])
    total_burndown = list(total_burndown.values())
    total_burndown.sort(key=lambda item: item["date"])
    combined_burndown["data"] = list(combined_burndown["data"].values())
    combined_burndown["data"].sort(key=lambda item: item["date"])

    return {
        "partial_burndown": {
            "partial_burndown_data": partial_burndown,
        },
        "bv_burndown": {
            "bv_burndown_data": bv_burndown
        },
        "total_burndown": {
            "total_burndown_data": total_burndown
        },
        "combined_burndown": combined_burndown,
        "sprint": milestone["name"],
        "total_sp": combined_burndown["total_story_points"],
        "total_bv": combined_burndown["total_business_value"]
    }


def calc_burndown_day_data(auth_token, milestone, attribute_key):
    days_data = {}
    days_bv_data = {}
    days_total_data = {}
    combined_data = {}
    start = datetime.fromisoformat(milestone["estimated_start"])
    finish = datetime.fromisoformat(milestone["estimated_finish"])
    milestone_start = start.date()
    milestone_finish = finish.date()

    if milestone["total_points"] is None:
        milestone["total_points"] = 0

    days_data[milestone_start] = append_points_date_data(
        milestone_start, 0, milestone["total_points"]
    )
    days_data[milestone_start]["day"] = 0
    days_data[milestone_start]["expected_remaining"] = (
        milestone["total_points"]
    )

    days_total_data[milestone_start] = append_points_date_data(
        milestone_start, 0, milestone["total_points"]
    )
    days_total_data[milestone_start]["day"] = 0
    days_total_data[milestone_start]["expected_remaining"] = (
        milestone["total_points"]
    )

    days_bv_data[milestone_start] = {
        "date": milestone_start,
        "completed": 0,
        "day": 0
    }

    total_business_value = {"bv": 0}
    with ThreadPoolExecutor(max_workers=15) as executor:
        for user_story in milestone["user_stories"]:
            executor.submit(process_burndown_details, user_story, auth_token,
                            total_business_value, days_data, attribute_key,
                            days_bv_data, days_total_data)

    expected_decrement = round(
        milestone["total_points"] / (finish - start).days, 2
    )
    update_points_days_data(
        days_data, milestone_start, milestone_finish, expected_decrement
    )
    update_points_days_data(
        days_total_data, milestone_start, milestone_finish, expected_decrement
    )

    days_bv_data[milestone_start]["remaining"] = total_business_value["bv"]
    days_bv_data[milestone_start]["expected_remaining"] = (
        total_business_value["bv"]
    )
    expected_bv_decrement = round(
        (total_business_value["bv"])/(finish - start).days, 2
    )
    update_bv_days_data(
        days_bv_data, milestone_start, milestone_finish, expected_bv_decrement
    )

    combined_data = {
        "total_story_points": milestone["total_points"],
        "total_business_value": total_business_value["bv"],
        "data": {}
    }

    extract_combined_data(
        combined_data,
        days_data,
        days_bv_data,
        days_total_data
    )

    return days_data, days_bv_data, days_total_data, combined_data


def extract_combined_data(
    combined_data,
    days_data,
    days_bv_data,
    days_total_data
):
    total_sp = combined_data["total_story_points"]
    total_bv = combined_data["total_business_value"]
    for dt in days_data:
        combined_data["data"][dt] = {
            "date": dt,
            "day": days_data[dt]["day"],
            "remaining_sp": days_total_data[dt]["remaining"],
            "remaining_bv": days_bv_data[dt]["remaining"],
            "partial": round((
                ((days_data[dt]["remaining"]) * 100)
                / total_sp
            ), 2) if total_sp != 0 else 0,
            "total": round((
                ((days_total_data[dt]["remaining"]) * 100)
                / total_sp
            ), 2) if total_sp != 0 else 0,
            "bv": round((
                ((days_bv_data[dt]["remaining"]) * 100)
                / total_bv
            ), 2) if total_bv != 0 else 0
        }


def process_burndown_details(
        user_story, auth_token, total_business_value, days_data, attribute_key,
        days_bv_data, days_total_data
):
    tasks = get_tasks_by_story_id(user_story["id"], auth_token)
    extract_partial_burndown_data(user_story, tasks, days_data)

    business_value = get_business_value(
        user_story["id"], attribute_key, auth_token
    )
    total_business_value["bv"] = (
        total_business_value["bv"] + int(business_value)
    )
    extract_bv_burndown_data(user_story, int(business_value), days_bv_data)

    extract_total_burndown_data(user_story, days_total_data)


def update_points_days_data(
        days_data, milestone_start, milestone_finish, expected_decrement
):
    for dt in daterange(
        milestone_start + timedelta(1), milestone_finish + timedelta(1)
    ):
        if dt not in days_data:
            days_data[dt] = append_points_date_data(
                datetime.fromisoformat(str(dt)).date(), 0,
                days_data[dt - timedelta(1)]["remaining"])
            days_data[dt]["day"] = (
                days_data[dt - timedelta(1)]["day"] + 1
            )
        else:
            days_data[dt]["remaining"] = round(
                days_data[dt - timedelta(1)]["remaining"]
                - days_data[dt]["completed"], 2)
            days_data[dt]["day"] = (
                days_data[dt - timedelta(1)]["day"] + 1
            )

        days_data[dt]["expected_remaining"] = round(
            days_data[dt - timedelta(1)]["expected_remaining"]
            - expected_decrement, 2)

        if days_data[dt]["expected_remaining"] < 0:
            days_data[dt]["expected_remaining"] = 0

    for dt in days_data:
        if "day" not in days_data[dt]:
            days_data[dt]["day"] = (
                days_data[dt - timedelta(1)]["day"] + 1
            )
            days_data[dt]["expected_remaining"] = (
                days_data[dt - timedelta(1)]["expected_remaining"]
            )
            days_data[dt]["remaining"] = round(
                days_data[dt - timedelta(1)]["remaining"]
                - days_data[dt]["completed"], 2)


def update_bv_days_data(
        days_bv_data, milestone_start, milestone_finish, expected_bv_decrement
):
    for dt in daterange(
        milestone_start + timedelta(1), milestone_finish + timedelta(1)
    ):
        if dt not in days_bv_data:
            days_bv_data[dt] = {
                "date": datetime.fromisoformat(str(dt)).date(),
                "completed": 0,
                "remaining": days_bv_data[dt - timedelta(1)]["remaining"],
                "day": days_bv_data[dt - timedelta(1)]["day"] + 1
            }
        else:
            days_bv_data[dt]["remaining"] = round(
                days_bv_data[dt - timedelta(1)]["remaining"]
                - days_bv_data[dt]["completed"], 2)
            days_bv_data[dt]["day"] = (
                days_bv_data[dt - timedelta(1)]["day"] + 1
            )

        days_bv_data[dt]["expected_remaining"] = (
            round(days_bv_data[dt - timedelta(1)]["expected_remaining"]
                  - expected_bv_decrement, 2)
        )

        if days_bv_data[dt]["expected_remaining"] < 0:
            days_bv_data[dt]["expected_remaining"] = 0

    for dt in days_bv_data:
        if "day" not in days_bv_data[dt]:
            days_bv_data[dt]["day"] = (
                days_bv_data[dt - timedelta(1)]["day"] + 1
            )
            days_bv_data[dt]["expected_remaining"] = (
                days_bv_data[dt - timedelta(1)]["expected_remaining"]
            )
            days_bv_data[dt]["remaining"] = round(
                days_bv_data[dt - timedelta(1)]["remaining"]
                - days_bv_data[dt]["completed"], 2)


def extract_partial_burndown_data(user_story, tasks, days_data):
    for task in tasks:
        if task["is_closed"]:
            finished_date = datetime.fromisoformat(
                task["finished_date"]).date()
            if user_story["total_points"] is None:
                user_story["total_points"] = 0
            partial_story_points = round(
                user_story["total_points"]/len(tasks), 2)

            if finished_date in days_data:
                days_data[finished_date]["completed"] = (
                    days_data[finished_date]["completed"]
                    + partial_story_points
                )
            else:
                days_data[finished_date] = append_points_date_data(
                    finished_date, partial_story_points, 0
                )


def extract_bv_burndown_data(user_story, business_value, days_bv_data):
    if user_story["is_closed"]:
        finished_date = datetime.fromisoformat(
            user_story["finish_date"]).date()
        if finished_date in days_bv_data:
            days_bv_data[finished_date]["completed"] = (
                days_bv_data[finished_date]["completed"] + business_value
            )
        else:
            days_bv_data[finished_date] = {
                "date": finished_date,
                "completed": business_value,
                "remaining": 0
            }


def extract_total_burndown_data(user_story, days_total_data):
    if user_story["is_closed"]:
        finished_date = datetime.fromisoformat(
            user_story["finish_date"]).date()
        if user_story["total_points"] is None:
            user_story["total_points"] = 0
        if finished_date in days_total_data:
            days_total_data[finished_date]["completed"] = (
                days_total_data[finished_date]["completed"]
                + user_story["total_points"]
            )
        else:
            days_total_data[finished_date] = append_points_date_data(
                finished_date, user_story["total_points"], 0
            )


def append_points_date_data(
        date, completed_story_points, remaining_story_points
):
    return {
        "date": date,
        "completed": completed_story_points,
        "remaining": remaining_story_points
    }


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
