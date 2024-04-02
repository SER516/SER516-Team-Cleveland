import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


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
