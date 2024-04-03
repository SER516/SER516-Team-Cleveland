import os
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv
from datetime import datetime
from userStory.get_user_story_history import (
    get_user_story,
    get_closed_user_stories
)

# Load environment variables from .env file
load_dotenv()


def get_us_lead_time(project_id, auth_token, from_date=None, to_date=None):
    user_stories = get_closed_user_stories(project_id, auth_token)
    lead_time = 0
    closed_user_stories = 0
    lead_times = []
    for user_story in user_stories:
        created_date = datetime.fromisoformat(user_story["created_date"])
        finished_date = datetime.fromisoformat(user_story['finished_date'])
        if from_date is not None and from_date > finished_date.date():
            continue
        if to_date is not None and to_date < finished_date.date():
            continue
        lead_time += (finished_date - created_date).days
        lead_times.append({
            "taskDesc": user_story["subject"],
            "sprintURL": user_story["sprintURL"],
            "taskRef": user_story["ref"],
            "taskId": user_story["id"],
            "startTime": user_story["created_date"],
            "startDate": created_date.date(),
            "endTime": user_story['finished_date'],
            "endDate": finished_date.date(),
            "timeTaken": (finished_date - created_date).days
        })
        closed_user_stories += 1
    if closed_user_stories == 0:
        return lead_times, 0
    avg_lead_time = round((lead_time / closed_user_stories), 2)
    return lead_times, avg_lead_time


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
    task_history_url = f"{taiga_url}/history/userstory/{story['id']}"
    finished_date = story["finished_date"]
    try:
        response = requests.get(task_history_url, headers=headers)
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


def get_zero_bv_us(
    project_id,
    start_range,
    end_range,
    auth_token
):
    user_stories = get_closed_user_stories(project_id, auth_token)
    user_stories_in_range = []
    start_range_date = datetime.strptime(start_range, '%Y-%m-%d')
    start_range_date = start_range_date.date()
    end_range_date = datetime.strptime(end_range, "%Y-%m-%d")
    end_range_date = end_range_date.date()
    for user_story in user_stories:
        endTime = datetime.fromisoformat(user_story["finished_date"]).date()
        if endTime >= start_range_date and endTime <= end_range_date:
            user_stories_in_range.append(user_story)

    return user_stories_in_range
