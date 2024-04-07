from fastapi import APIRouter, Header
from typing import Annotated

from model.burndownChartRequest import BurndownChartRequest
from service.burndown_service import (
    get_burndown_chart_metric_detail,
    get_multi_sprint_data
)

router = APIRouter()


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