import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from datetime import datetime

from .getTasks import task_by_member_in_date_range
from tasks.get_tasks import (
    get_closed_tasks
)
from tasks.get_task_history import (
    get_task_details,
    dev_focus_tasks,
    sorted_tasks_data
)

# Load environment variables from .env file
load_dotenv()


def get_task_lead_time(project_id, auth_token, from_date=None, to_date=None):
    tasks = get_closed_tasks(project_id, auth_token)
    lead_time = 0
    closed_tasks = 0
    lead_times = []
    for task in tasks:
        created_date = datetime.fromisoformat(task["created_date"])
        finished_date = datetime.fromisoformat(task['finished_date'])
        if from_date is not None and from_date > finished_date.date():
            continue
        if to_date is not None and to_date < finished_date.date():
            continue
        lead_time += (finished_date - created_date).days
        lead_times.append({
            "taskDesc": task["subject"],
            "sprintURL": task["sprintURL"],
            "taskRef": task["ref"],
            "taskId": task["id"],
            "startTime": task["created_date"],
            "startDate": created_date.date(),
            "endTime": task['finished_date'],
            "endDate": finished_date.date(),
            "timeTaken": (finished_date - created_date).days
        })
        closed_tasks += 1
    if closed_tasks == 0:
        return lead_times, 0
    avg_lead_time = round((lead_time / closed_tasks), 2)

    return lead_times, avg_lead_time


# Function to extract the date when a task transitioned from
# 'New' to 'In progress'
def extract_new_to_in_progress_date(history_data):
    for event in history_data:
        values_diff = event.get("values_diff", {})
        if (
            "status" in values_diff and
            values_diff["status"] == ["New", "In progress"]
        ):
            created_at = datetime.fromisoformat(event["created_at"])
            return created_at
    return None


def extract_state_change_dates(history_data):
    in_progress_date, closed_at = None, None
    for event in history_data:
        values_diff = event.get("values_diff", {})
        if "status" in values_diff:
            if values_diff["status"] == ["New", "In progress"]:
                in_progress_date = datetime.fromisoformat(event["created_at"])
            if (values_diff["status"] == ['In progress', 'DONE'] or
                    values_diff["status"] == ['Ready for test', 'DONE']):
                closed_at = datetime.fromisoformat(event["created_at"])
    return in_progress_date, closed_at


def get_task_cycle_time(project_id, auth_token, from_date=None, to_date=None):
    tasks = get_closed_tasks(project_id, auth_token)
    taiga_url = os.getenv('TAIGA_URL')

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    cycle_times = []
    cycle_time_data = {
        "closed_tasks": 0,
        "cycle_time": 0
    }
    with ThreadPoolExecutor(max_workers=15) as executor:
        for task in tasks:
            finished_date = datetime.fromisoformat(task['finished_date'])
            if from_date is not None and from_date > finished_date.date():
                continue
            if to_date is not None and to_date < finished_date.date():
                continue
            executor.submit(
                get_task_details,
                task,
                headers,
                taiga_url,
                cycle_times,
                cycle_time_data
            )

    if cycle_time_data["closed_tasks"] == 0:
        return cycle_times, 0

    avg_cycle_time = round(
        (cycle_time_data["cycle_time"] / cycle_time_data["closed_tasks"]),
        2
    )
    return cycle_times, avg_cycle_time


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
