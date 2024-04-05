from datetime import date, datetime
from userStory.get_user_story_history import get_closed_user_stories
from tasks.get_tasks import get_closed_tasks


def get_lead_time_details(project_details,
                          auth_token,
                          from_date=None,
                          to_date=None):
    if from_date is not None and len(from_date) > 0:
        from_date = date.fromisoformat(from_date)
    if to_date is not None and len(to_date) > 0:
        to_date = date.fromisoformat(to_date)
    us_lead_time, avg_us_lt = get_us_lead_time(
        project_details["id"], auth_token, from_date, to_date
    )
    task_lead_time, avg_task_lt = get_task_lead_time(
        project_details["id"], auth_token, from_date, to_date
    )

    us_lead_time.sort(key=lambda item: item["endDate"])
    task_lead_time.sort(key=lambda item: item["endDate"])

    # get objects created that store the details
    # for task and user story lead times
    us_lead_time = get_lead_time_object("userStory", us_lead_time, avg_us_lt)
    task_lead_time = get_lead_time_object("task", task_lead_time, avg_task_lt)

    lead_time = {
        "storiesLeadTime": us_lead_time,
        "tasksLeadTime": task_lead_time
    }
    return metric_object("LEAD", "leadTime", lead_time, project_details)


def get_lead_time_object(object_type, task_lead_time, avg_task_lt):
    return {
        object_type: task_lead_time,
        "avgLeadTime": avg_task_lt
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


def get_us_lead_time(project_id, auth_token, from_date=None, to_date=None):
    user_stories = get_closed_user_stories(project_id, auth_token)
    lead_time = 0
    closed_user_stories = 0
    lead_times = []
    for user_story in user_stories:
        created_date = date.fromisoformat(user_story["created_date"])
        finished_date = date.fromisoformat(user_story['finished_date'])
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
