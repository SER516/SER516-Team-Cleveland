from fastapi import APIRouter, Header
from typing import Annotated

from project.getProjectBySlug import get_project_by_slug
from service.cycle_time_service import get_cycle_time_details
from model.cycle_time_model import TimeRequest
from service.simple_cache import cache

router = APIRouter()


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