import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_tasks(project_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    task_api_url = f"{taiga_url}/tasks?project={project_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:
        response = requests.get(task_api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks: {e}")
        return None


def get_closed_tasks(project_id, auth_token):
    tasks = get_tasks(project_id, auth_token)
    if tasks:
        closed_tasks = [
            {
                "id": task["id"],
                "subject": task["subject"],
                "created_date": task["created_date"],
                "finished_date": task["finished_date"],
                "ref": task["ref"],
                "sprintURL": task["project_extra_info"]["slug"]
            }
            for task in tasks if task.get("is_closed")
        ]

        return closed_tasks
    else:
        return []


def get_tasks_by_story_id(user_story_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    user_story_id = f"{taiga_url}/tasks?user_story={user_story_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:
        response = requests.get(user_story_id, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching User Story with id {user_story_id}", e)
        return None


def get_task_for_member(project_id, member_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    task_by_member = f"""
        {taiga_url}/tasks?assigned_to={member_id}&project={project_id}"""

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:
        response = requests.get(task_by_member, headers=headers)

        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks with member id {member_id}", e)
        return None
