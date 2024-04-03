from fastapi import APIRouter

router = APIRouter()


@router.post("/metric/LeadTime")
def get_lead_time_metric():
    return {
        "message": "hello"
    }
