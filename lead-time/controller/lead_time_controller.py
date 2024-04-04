from fastapi import APIRouter, Header
from typing import Annotated

from pydantic import BaseModel
from datetime import date

router = APIRouter()


class TimeRequest(BaseModel):
    projectslug: str
    from_date: str = None
    to_date: str = None


class SimpleCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()


# Create an instance of SimpleCache that can be imported in other files
cache = SimpleCache()


@router.post("/metric/LeadTime")
def get_lead_time_metric(
    lead_time_request: TimeRequest,
    token: Annotated[str | None, Header()] = None
):
    if cache.get(lead_time_request.projectslug) is None:
        project_info = get_project_by_slug(
            lead_time_request.projectslug,
            token
        )
        cache.set(lead_time_request.projectslug, project_info)
        return get_lead_time_details(
            project_info,
            token,
            lead_time_request.from_date,
            lead_time_request.to_date
        )
    else:
        return get_lead_time_details(
            cache.get(lead_time_request.projectslug),
            token,
            lead_time_request.from_date,
            lead_time_request.to_date
        )


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

    us_lead_time.sort(key=lambda item: item["endDate"])

    us_lead_time = get_lead_time_object("userStory", us_lead_time, avg_us_lt)

    lead_time = {
        "storiesLeadTime": us_lead_time,
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
