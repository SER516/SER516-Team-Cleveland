from dotenv import load_dotenv

from tasks.get_tasks import (
    get_task_for_member
)

# Load environment variables from a .env file
load_dotenv()


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
