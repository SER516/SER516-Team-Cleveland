from fastapi import APIRouter, Header
from typing import Annotated

from service.lead_time_service import get_lead_time_details
from model.lead_time_model import TimeRequest
from service.simle_service import cache
from library.project.getProjectBySlug import get_project_by_slug

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
