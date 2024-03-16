import os
from concurrent.futures import ThreadPoolExecutor
import requests
from dotenv import load_dotenv
from datetime import datetime

from .getTasks import get_closed_tasks, task_by_member_in_date_range

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
            # Raise an exception for HTTP errors (4xx or 5xx)
            response.raise_for_status()
            history_data = response.json()

            # Extract the date when the task transitioned from
            # 'New' to 'In progress'
            in_progress_date = extract_new_to_in_progress_date(history_data)

            # Convert finished_date and in_progress_date to datetime objects
            finished_date = datetime.fromisoformat(finished_date[:-1])
            if in_progress_date:
                in_progress_date = datetime.fromisoformat(
                    str(in_progress_date)[:-6]
                )

                # Calculate cycle time and increment closed_tasks count
                cycle_time += (finished_date - in_progress_date).days
                closed_tasks += 1

        except requests.exceptions.RequestException as e:
            # Handle errors during the API request and print an error message
            print(f"Error fetching project by slug: {e}")

    # Return a list containing cycle_time and closed_tasks count
    return [cycle_time, closed_tasks]


def get_task_details(task, headers, taiga_url, cycle_times, cycle_time_data):
    task_history_url = f"{taiga_url}/history/task/{task['id']}"
    finished_date = task["finished_date"]
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
                "taskId": task["id"],
                "taskDesc": task["subject"],
                "taskRef": task["ref"],
                "startTime": task["created_date"],
                "inProgressDate": in_progress_date.date(),
                "endTime": task['finished_date'],
                "endDate": finished_date.date(),
                "timeTaken": (finished_date - in_progress_date).days
            })
            cycle_time_data["closed_tasks"] += 1
            cycle_time_data["cycle_time"] += (
                finished_date - in_progress_date
            ).days

    except requests.exceptions.RequestException as e:
        print(f"Error fetching task by taskId: {e}")


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


def get_task_cycle_time(project_id, auth_token):
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


def dev_focus_tasks(
    task,
    headers,
    taiga_url,
    from_date,
    to_date,
    dev_focus_data
):
    task_history_url = f"{taiga_url}/history/task/{task['id']}"
    try:
        response = requests.get(task_history_url, headers=headers)
        response.raise_for_status()
        history_data = response.json()
        in_progress_date = extract_new_to_in_progress_date(history_data)

        if in_progress_date:
            in_progress_date = datetime.fromisoformat(
                str(in_progress_date)[:-6]
            )

            if (
                in_progress_date > datetime.fromisoformat(from_date) and
                in_progress_date < datetime.fromisoformat(to_date)
            ):
                dev_focus_data.append({
                    "taskId": task["id"],
                    "taskDesc": task["subject"],
                    "taskRef": task["ref"],
                    "created_date": task["created_date"],
                    "inProgressDate": in_progress_date.date(),
                    "username": task["username"],
                    "full_name": task["full_name"]
                })

    except requests.exceptions.RequestException as e:
        print(f"Error fetching task by taskId: {e}")


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


def sorted_tasks_data(
    task,
    headers,
    taiga_url,
    from_date,
    to_date,
    member_tasks
):
    task_history_url = f"{taiga_url}/history/task/{task['id']}"
    try:
        response = requests.get(task_history_url, headers=headers)
        response.raise_for_status()
        history_data = response.json()
        in_progress_date, closed_date = extract_state_change_dates(
            history_data
        )
        if (in_progress_date is not None or closed_date is not None):
            in_progress_date = datetime.fromisoformat(
                str(in_progress_date)[:-6]
            ) if in_progress_date is not None else None
            closed_date = datetime.fromisoformat(
                str(closed_date)[:-6]
            ) if closed_date is not None else None

            if (
                (
                    in_progress_date is not None
                    and datetime.fromisoformat(from_date) < in_progress_date
                    < datetime.fromisoformat(to_date)
                ) or
                (
                    closed_date is not None
                    and datetime.fromisoformat(from_date) < closed_date
                    < datetime.fromisoformat(to_date)
                )
            ):
                task_data = {
                    "taskId": task["id"],
                    "taskDesc": task["subject"],
                    "taskRef": task["ref"],
                    "created_date": task["created_date"],
                    "inProgressDate": in_progress_date
                    if in_progress_date is not None
                    else datetime.fromisoformat(
                        task["created_date"]
                    ).replace(tzinfo=None),
                    "closed_date": closed_date,
                    "finished_date": task["finished_date"],
                    "username": task["username"],
                    "full_name": task["full_name"]
                }
                if task["username"] in member_tasks:
                    member_tasks[task["username"]].append(task_data)
                else:
                    member_tasks[task["username"]] = [task_data]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching task by taskId: {e}")
