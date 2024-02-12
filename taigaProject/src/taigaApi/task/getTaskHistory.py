import os
import requests
from dotenv import load_dotenv
from datetime import datetime

from .getTasks import get_closed_tasks

from taigaApi.task.getTasks import get_closed_tasks

from .getTasks import get_closed_tasks

# Load environment variables from .env file
load_dotenv()


# Function to retrieve task history and calculate cycle time for closed tasks
def get_task_history(tasks, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    # Initialize variables to store cycle time and count of closed tasks
    cycle_time = 0
    closed_tasks = 0

    # Iterate over each task to retrieve task history and calculate cycle time
    for task in tasks:
        task_history_url = f"{taiga_url}/history/task/{task['id']}"
        finished_date = task["finished_date"]
        try:
            # Make a GET request to Taiga API to retrieve task history
            response = requests.get(task_history_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            history_data = response.json()

            # Extract the date when the task transitioned from 'New' to 'In progress'
            in_progress_date = extract_new_to_in_progress_date(history_data)

            # Convert finished_date and in_progress_date to datetime objects
            finished_date = datetime.fromisoformat(finished_date[:-1])
            if in_progress_date:
                in_progress_date = datetime.fromisoformat(str(in_progress_date)[:-6])

                # Calculate cycle time and increment closed_tasks count
                cycle_time += (finished_date - in_progress_date).days
                closed_tasks += 1

        except requests.exceptions.RequestException as e:
            # Handle errors during the API request and print an error message
            print(f"Error fetching project by slug: {e}")

    # Return a list containing cycle_time and closed_tasks count
    return [cycle_time, closed_tasks]


def get_task_lead_time(project_id, auth_token):
    tasks = get_closed_tasks(project_id, auth_token)
    lead_time = 0
    closed_tasks = 0
    lead_times = []
    for task in tasks:
        created_date = datetime.fromisoformat(task["created_date"])
        finished_date = datetime.fromisoformat(task['finished_date'])
        lead_time += (finished_date - created_date).days
        lead_times.append({
            "taskId": task["id"],
            "startTime": task["created_date"],
            "startTime": created_date.date(),
            "endTime": task['finished_date'],
            "endDate": finished_date.date(),
            "timeTaken": (finished_date - created_date).days
        })
        closed_tasks += 1
    if closed_tasks == 0:
        return lead_times, 0
    avg_lead_time = round((lead_time / closed_tasks), 2)

    return lead_times, avg_lead_time


# Function to extract the date when a task transitioned from 'New' to 'In progress'
def extract_new_to_in_progress_date(history_data):
    for event in history_data:
        values_diff = event.get("values_diff", {})
        if "status" in values_diff and values_diff["status"] == ["New", "In progress"]:
            created_at = datetime.fromisoformat(event["created_at"])
            return created_at
    return None


def get_task_cycle_time(project_id, auth_token):
    tasks = get_closed_tasks(project_id, auth_token)
    taiga_url = os.getenv('TAIGA_URL')

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    cycle_time = 0
    closed_tasks = 0
    cycle_times = []

    for task in tasks:
        task_history_url = f"{taiga_url}/history/task/{task['id']}"
        finished_date = task["finished_date"]
        try:
            response = requests.get(task_history_url, headers=headers)
            response.raise_for_status()
            history_data = response.json()

            in_progress_date = extract_new_to_in_progress_date(history_data)

            finished_date = datetime.fromisoformat(finished_date[:-1])
            if in_progress_date:
                in_progress_date = datetime.fromisoformat(str(in_progress_date)[:-6])

                cycle_time += (finished_date - in_progress_date).days
                cycle_times.append({
                    "taskId": task["id"],
                    "startTime": task["created_date"],
                    "inProgressDate": in_progress_date.date(),
                    "endTime": task['finished_date'],
                    "endDate": finished_date.date(),
                    "timeTaken": (finished_date - in_progress_date).days
                })
                closed_tasks += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching task by taskId: {e}")

    if closed_tasks == 0:
        return cycle_times, 0
    
    avg_cycle_time = round((cycle_time / closed_tasks), 2)
    return cycle_times, avg_cycle_time
