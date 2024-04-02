from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone, date
import itertools

from ..task.get_task_history import get_task_lead_time, get_task_cycle_time, \
    get_all_dev_focus, member_tasks
from ..userStory.get_user_story_history import get_us_lead_time, \
    get_us_cycle_time, get_zero_bv_us
from ..milestone.get_milestone import get_milestone
from tasks.get_tasks import get_tasks_by_story_id
from userStory.getBusinessValue import get_business_value


def get_lead_time_details(project_details,
                          auth_token,
                          from_date=None,
                          to_date=None):
    if from_date is not None and len(from_date) > 0:
        from_date = date.fromisoformat(from_date)
    if to_date is not None and len(to_date) > 0:
        to_date = date.fromisoformat(to_date)
    us_lead_time, avg_us_lt = get_us_lead_time(
        project_details["id"], auth_token, from_date, to_date
    )
    task_lead_time, avg_task_lt = get_task_lead_time(
        project_details["id"], auth_token, from_date, to_date
    )

    us_lead_time.sort(key=lambda item: item["endDate"])
    task_lead_time.sort(key=lambda item: item["endDate"])

    # get objects created that store the details
    # for task and user story lead times
    task_lead_time = get_lead_time_object("task", task_lead_time, avg_task_lt)
    us_lead_time = get_lead_time_object("userStory", us_lead_time, avg_us_lt)

    lead_time = {
        "storiesLeadTime": us_lead_time,
        "tasksLeadTime": task_lead_time
    }
    return metric_object("LEAD", "leadTime", lead_time, project_details)


def get_lead_time_object(object_type, task_lead_time, avg_task_lt):
    return {
        object_type: task_lead_time,
        "avgLeadTime": avg_task_lt
    }


def metric_object(metric, time_key, lead_time, project_details):
    return {
        "metric": metric,
        time_key: lead_time,
        "projectInfo": {
            "name": project_details["name"],
            "members": project_details["members"]
        }
    }


def get_cycle_time_details(project_details,
                           auth_token,
                           from_date=None,
                           to_date=None):
    if from_date is not None and len(from_date) > 0:
        from_date = date.fromisoformat(from_date)
    if to_date is not None and len(to_date) > 0:
        to_date = date.fromisoformat(to_date)
    task_cycle_time, avg_task_ct = get_task_cycle_time(
        project_details["id"], auth_token, from_date, to_date
    )
    us_cycle_time, avg_us_ct = get_us_cycle_time(
        project_details["id"], auth_token, from_date, to_date
    )

    task_cycle_time.sort(key=lambda item: item["endDate"])
    us_cycle_time.sort(key=lambda item: item["endDate"])

    task_cycle_time = get_cycle_time_object(
        "task", task_cycle_time, avg_task_ct
    )
    us_cycle_time = get_cycle_time_object(
        "story", us_cycle_time, avg_us_ct
    )

    cycle_time = {
        "taskCycleTime": task_cycle_time,
        "storyCycleTime": us_cycle_time
    }
    return metric_object("CYCLE", "cycleTime", cycle_time, project_details)


def get_cycle_time_object(object_type, cycle_time, avg_lt):
    return {
        object_type: cycle_time,
        "avgCycleTime": avg_lt
    }


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


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def daterangefloor(start_date, end_date):
    floor_date = datetime(start_date.year, start_date.month, start_date.day)
    for n in range(int((end_date - start_date).days)):
        yield floor_date + timedelta(n)


def append_points_date_data(
        date, completed_story_points, remaining_story_points
):
    return {
        "date": date,
        "completed": completed_story_points,
        "remaining": remaining_story_points
    }


def get_dev_focus_metric(
    project_id,
    from_date,
    to_date,
    threshold,
    members,
    auth_token
):
    dev_focus_data = get_all_dev_focus(
        project_id,
        from_date,
        to_date,
        threshold,
        members,
        auth_token
    )
    dev_focus = extract_dev_focus(dev_focus_data)

    output = {
        "date_data": dev_focus["date_data"]
    }

    members, total_violations = get_member_violations(dev_focus, threshold)
    output["members"] = members
    output["total_violations"] = total_violations

    return output


def extract_dev_focus(dev_focus_data):
    dev_focus = {}
    dev_focus["date_data"] = {}
    dev_focus["members"] = []

    for task in dev_focus_data:
        in_progress_date = datetime.fromisoformat(
            str(task["inProgressDate"])
        ).date()
        if in_progress_date in dev_focus["date_data"]:
            dev_focus["date_data"][in_progress_date]["total_violations"] += 1

            member = check_member_exist(
                dev_focus["date_data"][in_progress_date]["members"],
                task["username"]
            )
            if member:
                violations = member["violations"] + 1
                tasks = member["tasks"]
                tasks.append(task["taskId"])
                (
                    dev_focus["date_data"][in_progress_date]["members"]
                ).remove(member)

                dev_focus["date_data"][in_progress_date]["members"].append({
                    "name": task["full_name"],
                    "username": task["username"],
                    "violations": violations,
                    "tasks": tasks
                })

            else:
                dev_focus["date_data"][in_progress_date]["members"].append({
                    "name": task["full_name"],
                    "username": task["username"],
                    "violations": 1,
                    "tasks": [task["taskId"]]
                })

        else:
            dev_focus["date_data"][in_progress_date] = {
                "date": in_progress_date,
                "total_violations": 1,
                "members": [
                    {
                        "name": task["full_name"],
                        "username": task["username"],
                        "violations": 1,
                        "tasks": [task["taskId"]]
                    }
                ]
            }

    return dev_focus


def get_member_violations(dev_focus, threshold):
    total_violations = 0
    members = []
    for date_data in list(dev_focus["date_data"]):
        total_violations += len(dev_focus["date_data"][date_data]["members"])
        for member in dev_focus["date_data"][date_data]["members"]:
            if member["violations"] < threshold:
                dev_focus["date_data"][date_data]["total_violations"] -= (
                    member["violations"])
                dev_focus["date_data"][date_data]["members"].remove(member)
            else:
                member_2 = check_member_exist(members, member["username"])
                if not member_2:
                    members.append(member)
                else:
                    members.remove(member_2)

                    member.append(member)

        if dev_focus["date_data"][date_data]["total_violations"] == 0:
            dev_focus["date_data"].pop(date_data)

    return members, total_violations


def check_member_exist(members, username):
    for member in members:
        if member["username"] == username:
            return member
        else:
            return None


# def member_dev_focus()


def fetch_member_tasks(project_id, from_date, to_date, members, token):
    member_tasks_map = member_tasks(
        project_id,
        from_date,
        to_date,
        members,
        token
    )

    date_map = {}
    with ThreadPoolExecutor(max_workers=15) as executor:
        for key in member_tasks_map:
            executor.submit(
                dev_focus_data_map,
                key,
                member_tasks_map[key],
                date_map,
                from_date,
                to_date
            )
    for key in date_map:
        for date_key in date_map[key]:
            tasks_to_remove = []
            for task1, task2 in itertools.combinations(
                date_map[key][date_key], 2
            ):
                if (
                    all(value is not None for value in [
                        task1["inProgressDate"], task2["closed_date"]
                    ])
                    and task1["inProgressDate"] > task2["closed_date"]
                ):
                    tasks_to_remove.append(task1)
                elif (
                    all(value is not None for value in [
                        task2["inProgressDate"], task1["closed_date"]
                    ])
                    and task2["inProgressDate"] > task1["closed_date"]
                ):
                    tasks_to_remove.append(task2)

            # Remove tasks that need to be removed
            for task in tasks_to_remove:
                if task in date_map[key][date_key]:
                    date_map[key][date_key].remove(task)

    return date_map


def dev_focus_data_map(key, tasks, date_map, from_date, to_date):
    date_map[key] = {}
    try:
        for task in tasks:
            from_date_date, to_date_date = \
                datetime.fromisoformat(from_date), \
                datetime.fromisoformat(to_date)
            from_date_date = \
                from_date_date if task['inProgressDate'] is None \
                else max(task['inProgressDate'], from_date_date)
            to_date_date = min(to_date_date, datetime.now()) \
                if task['closed_date'] is None else min(
                    [task['closed_date'],
                     to_date_date,
                     datetime.now().utcnow()]
                )
            for single_date in daterange(
                from_date_date,
                to_date_date + timedelta(days=1)
            ):
                single_date_str = single_date.strftime("%m-%d-%Y")
                if single_date_str not in date_map[key]:
                    date_map[key][single_date_str] = []
                date_map[key][single_date_str].append(task)
        date_map[key] = {
            date_key: date_map[key][date_key]
            for date_key in sorted(date_map[key].keys())
        }

    except Exception as e:
        print(e)
        return date_map


def check_dates_overlap(
    task_1_inprogress_date,
    task_2_inprogress_date,
    task_1_finish_date,
    task_2_finish_date
):
    latest_start = max(task_1_inprogress_date, task_2_inprogress_date)
    earliest_end = min(task_1_finish_date, task_2_finish_date)
    delta = (earliest_end.date() - latest_start.date()).days + 1
    overlap = max(0, delta)
    if overlap == 0:
        return 0, 0
    else:
        return overlap, latest_start.date()


def check_still_in_progress(finished_date):
    if finished_date:
        return datetime.fromisoformat(finished_date)
    else:
        return datetime.now(timezone.utc)


def get_zero_business_value_user_stories(
    project_id,
    start_range,
    end_range,
    attribute_key,
    auth_token
):
    user_stories = get_zero_bv_us(
        project_id,
        start_range,
        end_range,
        auth_token
    )
    zero_bv_user_stories = []
    total_story_points = 0
    zero_bv_story_points = 0
    for user_story in user_stories:
        if user_story["story_points"] is None:
            continue
        total_story_points += int(user_story["story_points"])
        business_value = get_business_value(
            user_story["id"],
            attribute_key,
            auth_token
        )
        if business_value == "0":
            zero_bv_story_points += int(user_story["story_points"])
            zero_bv_user_stories.append(user_story)

    cruft_details = {"zero_bv_user_stories": zero_bv_user_stories,
                     "total_user_stories": len(user_stories),
                     "total_zero_bv_user_stories": len(zero_bv_user_stories),
                     "total_story_points": total_story_points,
                     "total_zero_bv_story_points": zero_bv_story_points}

    return cruft_details
