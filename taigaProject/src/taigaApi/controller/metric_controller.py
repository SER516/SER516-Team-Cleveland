from fastapi import APIRouter

from taigaApi.model.projectRequest import ProjectRequest
from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.util.metric_service import get_lead_time_details
from taigaApi.util.SimpleCache import cache

router = APIRouter()

@router.get("/metric/LeadTime")
def auth(projectRequest: ProjectRequest):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, projectRequest.authtoken)
        cache.set(projectRequest.projectslug, project_info)
        return get_lead_time_details(project_info, projectRequest.authtoken)
    else:
        return get_lead_time_details(cache.get(projectRequest.projectslug), projectRequest.authtoken)
