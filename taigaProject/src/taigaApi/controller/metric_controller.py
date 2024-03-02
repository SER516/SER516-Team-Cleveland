from fastapi import APIRouter, Header
from typing import Annotated

from taigaApi.model.projectRequest import ProjectRequest
from taigaApi.model.cruft import CruftRequest
from taigaApi.model.burndownChartRequest import BurndownChartRequest
from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.util.metric_service import (
    get_lead_time_details, 
    get_cycle_time_details,
    get_burndown_chart_metric_detail,
    get_zero_business_value_user_stories
)
from taigaApi.milestone.get_milestone import get_milestone
from taigaApi.util.SimpleCache import cache
from taigaApi.issues.get_issues import get_issues
from datetime import date

router = APIRouter()


@router.post("/metric/LeadTime")
def get_lead_time_metric(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        cache.set(projectRequest.projectslug, project_info)
        return get_lead_time_details(project_info, token)
    else:
        return get_lead_time_details(
            cache.get(projectRequest.projectslug), token
        )


@router.post("/metric/CycleTime")
def get_cycle_time_metric(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        cache.set(projectRequest.projectslug, project_info)
        return get_cycle_time_details(project_info, token)
    else:
        return get_cycle_time_details(
            cache.get(projectRequest.projectslug), token
        )


@router.post("/metric/Burndown")
def get_burndown_chart_metric(
    burndownChartRequest: BurndownChartRequest,
    token: Annotated[str | None, Header()] = None
):
    return get_burndown_chart_metric_detail(
        burndownChartRequest.milestoneId, 
        burndownChartRequest.attributeKey, token
    )

@router.post("/metric/Cruft")
def get_zero_business_value(
    cruftRequest: CruftRequest, 
    token: Annotated[str | None, Header()] = None
):
    zero_bv_stories = get_zero_business_value_user_stories(
        cruftRequest.projectId, 
        cruftRequest.startDate,
        cruftRequest.endDate,
        cruftRequest.attributeKey,
        token
    )
    issues = get_issues(
        cruftRequest.projectId,
        date.fromisoformat(cruftRequest.startDate),
        date.fromisoformat(cruftRequest.endDate),
        token
    )

    return {
        "zero_bv_us": zero_bv_stories,
        "issues": issues
    }
