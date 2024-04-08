import os

from dotenv import load_dotenv
from fastapi import APIRouter, Header
from typing import Annotated

from ..models.burndownChartRequest import BurndownChartRequest
from ..models.dev_focus_request import DevFocusRequest
from ..models.timeRequest import TimeRequest
from ..models.cruft import CruftRequest
from ..util.http_requests_util import post_call

router = APIRouter()
load_dotenv()


@router.post("/metric/LeadTime")
def get_lead_time_metric(
    lead_time_request: TimeRequest,
    token: Annotated[str | None, Header()] = None
):
    lt_url = os.getenv('METRICS_LEADTIME_URL')
    return post_call(lt_url, token, lead_time_request, 'metric/LeadTime')


@router.post("/metric/CycleTime")
def get_cycle_time_metric(
    cycle_time_request: TimeRequest,
    token: Annotated[str | None, Header()] = None
):
    ct_url = os.getenv('METRICS_CYCLETIME_URL')
    return post_call(ct_url, token, cycle_time_request, 'metric/CycleTime')


@router.post("/metric/Burndown")
def get_burndown_chart_metric(
    burndown_chart_request: BurndownChartRequest,
    token: Annotated[str | None, Header()] = None
):
    bd_url = os.getenv('METRICS_BURNDOWN_URL')
    return post_call(bd_url, token, burndown_chart_request, 'metric/Burndown')


@router.post("/metric/Devfocus")
def get_dev_focus_metrics(
    dev_focus_request: DevFocusRequest,
    token: Annotated[str | None, Header()] = None
):
    df_url = os.getenv('METRICS_DEV_FOCUS_URL')
    return post_call(df_url, token, dev_focus_request, 'metric/Devfocus')


@router.post("/metric/Cruft")
def get_zero_business_value(
    cruft_request: CruftRequest,
    token: Annotated[str | None, Header()] = None
):
    cruft_url = os.getenv('METRICS_CRUFT_URL')
    return post_call(cruft_url, token, cruft_request, 'metric/Cruft')
