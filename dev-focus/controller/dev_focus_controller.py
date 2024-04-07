from fastapi import APIRouter, Header
from typing import Annotated
from model.dev_focus_request import DevFocusRequest
from service.dev_focus_service import fetch_member_tasks

router = APIRouter()
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