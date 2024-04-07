from datetime import date

from fastapi import APIRouter, Header
from typing import Annotated

from issues.get_issues import get_issues

from model.cruft_model import CruftRequest
from service.cruft_service import get_zero_business_value_user_stories

router = APIRouter()


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
