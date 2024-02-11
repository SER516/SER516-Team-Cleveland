from fastapi import APIRouter, Header
from typing import Annotated

from taigaApi.model.projectRequest import ProjectRequest
from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.util.metric_service import get_lead_time_details
from taigaApi.util.SimpleCache import cache

router = APIRouter()

@router.post("/metric/LeadTime")
def get_lead_time_metric(projectRequest: ProjectRequest, token: Annotated[str | None, Header()] = None):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        cache.set(projectRequest.projectslug, project_info)
        return get_lead_time_details(project_info, token)
    else:
        return get_lead_time_details(cache.get(projectRequest.projectslug), token)
