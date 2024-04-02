from fastapi import APIRouter, Header
from typing import Annotated

from ..model.dev_focus_request import DevFocusRequest
from ..model.timeRequest import TimeRequest
from ..model.cruft import CruftRequest
from ..model.burndownChartRequest import BurndownChartRequest
from ..project.getProjectBySlug import get_project_by_slug
from ..util.metric_service import (
    get_lead_time_details,
    get_cycle_time_details,
    get_burndown_chart_metric_detail,
    get_zero_business_value_user_stories,
    fetch_member_tasks,
    get_multi_sprint_data
)
from ..util.SimpleCache import cache
from ..issues.get_issues import get_issues
from datetime import date

router = APIRouter()


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


@router.post("/metric/CycleTime")
def get_cycle_time_metric(
    cycle_time_request: TimeRequest,
    token: Annotated[str | None, Header()] = None
):
    if cache.get(cycle_time_request.projectslug) is None:
        project_info = get_project_by_slug(
            cycle_time_request.projectslug,
            token
        )
        cache.set(cycle_time_request.projectslug, project_info)
        return get_cycle_time_details(
            project_info, token,
            cycle_time_request.from_date,
            cycle_time_request.to_date
        )
    else:
        return get_cycle_time_details(
            cache.get(cycle_time_request.projectslug),
            token,
            cycle_time_request.from_date,
            cycle_time_request.to_date
        )


@router.post("/metric/Burndown")
def get_burndown_chart_metric(
    burndownChartRequest: BurndownChartRequest,
    token: Annotated[str | None, Header()] = None
):
    if burndownChartRequest.milestoneId is not None:
        return get_burndown_chart_metric_detail(
            burndownChartRequest.milestoneId,
            burndownChartRequest.attributeKey, token
        )
    elif len(burndownChartRequest.milestoneIds) == 1:
        return get_burndown_chart_metric_detail(
            burndownChartRequest.milestoneIds[0],
            burndownChartRequest.attributeKey, token
        )
    else:
        return get_multi_sprint_data(
            burndownChartRequest.milestoneIds,
            burndownChartRequest.attributeKey,
            token
        )


@router.post("/metric/Devfocus")
def get_dev_focus_metrics(
    dev_focus_request: DevFocusRequest,
    token: Annotated[str | None, Header()] = None
):
    return fetch_member_tasks(
        dev_focus_request.project_id,
        dev_focus_request.from_date,
        dev_focus_request.to_date,
        dev_focus_request.members,
        token
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
