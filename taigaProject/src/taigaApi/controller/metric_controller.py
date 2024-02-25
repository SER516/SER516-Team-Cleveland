from fastapi import APIRouter, Header
from typing import Annotated

from ..model.projectRequest import ProjectRequest
from ..model.burndownChartRequest import BurndownChartRequest
from ..project.getProjectBySlug import get_project_by_slug
from ..util.metric_service import get_lead_time_details, get_cycle_time_details, get_burndown_chart_metric_detail
from ..milestone.get_milestone import get_milestone
from ..util.SimpleCache import cache

router = APIRouter()

@router.post("/metric/LeadTime")
def get_lead_time_metric(projectRequest: ProjectRequest, token: Annotated[str | None, Header()] = None):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        cache.set(projectRequest.projectslug, project_info)
        return get_lead_time_details(project_info, token)
    else:
        return get_lead_time_details(cache.get(projectRequest.projectslug), token)


@router.post("/metric/CycleTime")
def get_cycle_time_metric(projectRequest: ProjectRequest, token: Annotated[str | None, Header()] = None):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        cache.set(projectRequest.projectslug, project_info)
        return get_cycle_time_details(project_info, token)
    else:
        return get_cycle_time_details(cache.get(projectRequest.projectslug), token)


@router.post("/metric/Burndown")
def get_burndown_chart_metric(burndownChartRequest: BurndownChartRequest, token: Annotated[str | None, Header()] = None):
    return get_burndown_chart_metric_detail(burndownChartRequest.milestoneId, burndownChartRequest.attributeKey, token)
