import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()


# Function to retrieve tasks for a specific project from the Taiga API
def get_tasks(project_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the tasks API endpoint for the specified project
    task_api_url = f"{taiga_url}/tasks?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:

        # Make a GET request to Taiga API to retrieve tasks
        response = requests.get(task_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Extract and return the tasks information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.RequestException as e:

        # Handle errors during the API request and print an error message
        print(f"Error fetching tasks: {e}")
        return None


# Function to retrieve closed tasks for a specific project from the Taiga API
def get_closed_tasks(project_id, auth_token):
    # Call the get_tasks function to retrieve all tasks for the project
    tasks = get_tasks(project_id, auth_token)
    if tasks:

        # Filter tasks to include only closed tasks and format the result
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


# Function to retrieve all tasks for a specific project from the Taiga API
def get_all_tasks(project_id, auth_token):
    # Call the get_tasks function to retrieve all tasks for the project
    tasks = get_tasks(project_id, auth_token)
    if tasks:

        # Format all tasks and return the result
        all_tasks = [
            {
                "id": task["id"],
                "created_date": task["created_date"],
                "finished_date": task["finished_date"]
            }
            for task in tasks
        ]

        return all_tasks
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
        print("Error fetching User Story with id {user_story_id}")
        return None


def get_task_for_member(project_id, member_id, auth_token):
    taiga_url = os.getenv('TAIGA_URL')

    task_by_member = f"{taiga_url}/tasks?assigned_to={member_id}&project={project_id}"

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
        print(f"Error fetching tasks with member id {member_id}")
        return None


def task_by_member_in_date_range(project_id, member_id, from_date, to_date, auth_token):
    tasks = get_task_for_member(project_id, member_id, auth_token)
    #filtering on the basis of when the task is created, IS_WRONG
    all_tasks = []
    for task in tasks:
        start_date = datetime.fromisoformat(task["created_date"]).date()

        all_tasks.append({
                "id": task["id"],
                "subject": task["subject"],
                "created_date": task["created_date"],
                "finished_date": task["finished_date"],
                "ref": task["ref"],
                "username": task["assigned_to_extra_info"]["username"],
                "full_name": task["assigned_to_extra_info"]["full_name_display"]
            })

    return all_tasks
