import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from datetime import datetime, date


from tasks.get_tasks import (
    get_closed_tasks
)
from tasks.get_task_history import (
    get_task_details
)
from userStory.get_user_story_history import (
    get_closed_user_stories,
    get_user_story_details_by_id
)
# Load environment variables from .env file
load_dotenv()

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


def metric_object(metric, time_key, lead_time, project_details):
    return {
        "metric": metric,
        time_key: lead_time,
        "projectInfo": {
            "name": project_details["name"],
            "members": project_details["members"]
        }
    }

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

def get_us_cycle_time(project_id, auth_token, from_date=None, to_date=None):
    user_stories = get_closed_user_stories(project_id, auth_token)
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
        for story in user_stories:
            finished_date = datetime.fromisoformat(story['finished_date'])
            if from_date is not None and from_date > finished_date.date():
                continue
            if to_date is not None and to_date < finished_date.date():
                continue
            executor.submit(
                get_user_story_details,
                story,
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


def get_user_story_details(
    story,
    headers,
    taiga_url,
    cycle_times,
    cycle_time_data
):
    response = get_user_story_details_by_id(story, headers, taiga_url)
    finished_date = story["finished_date"]
    try:
        response.raise_for_status()
        history_data = response.json()

        in_progress_date = extract_new_to_in_progress_date(history_data)

        finished_date = datetime.fromisoformat(finished_date[:-1])
        if in_progress_date:
            in_progress_date = datetime.fromisoformat(
                str(in_progress_date)[:-6]
            )

            cycle_times.append({
                "taskId": story["id"],
                "startTime": story["created_date"],
                "inProgressDate": in_progress_date.date(),
                "endTime": story['finished_date'],
                "endDate": finished_date.date(),
                "timeTaken": (finished_date - in_progress_date).days,
                "taskDesc": story["subject"],
                "sprintURL": story["sprintURL"],
                "taskRef": story["ref"]
            })
            cycle_time_data["closed_tasks"] += 1
            cycle_time_data["cycle_time"] += (
                finished_date - in_progress_date).days
    except requests.exceptions.RequestException as e:
        print(f"Error fetching task by taskId: {e}")