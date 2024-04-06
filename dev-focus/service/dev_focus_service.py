import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone, date
from dotenv import load_dotenv
from tasks.get_tasks import (
    get_task_for_member
)

from tasks.get_task_history import (
    get_task_details,
    dev_focus_tasks,
    sorted_tasks_data
)

import itertools

# Load environment variables from a .env file
load_dotenv()


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


def get_all_dev_focus(
        project_id,
        from_date,
        to_date,
        threshold,
        members,
        auth_token
):
    tasks = get_dev_focus(
        project_id,
        from_date,
        to_date,
        threshold,
        members,
        auth_token
    )
    taiga_url = os.getenv('TAIGA_URL')

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    dev_focus_data = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        for task in tasks:
            executor.submit(dev_focus_tasks, task, headers, taiga_url,
                            from_date, to_date, dev_focus_data)

    return dev_focus_data


def get_dev_focus(
        project_id,
        from_date,
        to_date,
        threshold,
        members,
        auth_token
):
    all_tasks = []
    for member in members:
        tasks = task_by_member_in_date_range(
            project_id,
            member,
            from_date,
            to_date,
            auth_token
        )
        all_tasks = all_tasks + tasks

    return all_tasks


def member_tasks(project_id, from_date, to_date, members, auth_token):
    member_tasks = {}
    with ThreadPoolExecutor(max_workers=15) as executor:
        for member in members:
            executor.submit(
                member_map,
                project_id,
                from_date,
                to_date,
                member,
                auth_token,
                member_tasks
            )
    return member_tasks


def member_map(
        project_id,
        from_date,
        to_date,
        member,
        auth_token,
        member_tasks
):
    tasks = task_by_member_in_date_range(
        project_id,
        member,
        from_date,
        to_date,
        auth_token
    )

    taiga_url = os.getenv('TAIGA_URL')

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    with ThreadPoolExecutor(max_workers=15) as executor:
        for task in tasks:
            executor.submit(sorted_tasks_data, task, headers, taiga_url,
                            from_date, to_date, member_tasks)


def check_member_exist(members, username):
    for member in members:
        if member["username"] == username:
            return member
        else:
            return None


def task_by_member_in_date_range(
        project_id,
        member_id,
        from_date,
        to_date,
        auth_token
):
    tasks = get_task_for_member(project_id, member_id, auth_token)
    # filtering on the basis of when the task is created, IS_WRONG
    all_tasks = []
    for task in tasks:
        all_tasks.append({
            "id": task["id"],
            "subject": task["subject"],
            "created_date": task["created_date"],
            "finished_date": task["finished_date"],
            "ref": task["ref"],
            "username": task["assigned_to_extra_info"]["username"],
            "full_name": (
                task["assigned_to_extra_info"]["full_name_display"]
            )
        })

    return all_tasks


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


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
