from pydantic import BaseModel


class BurndownChartRequest(BaseModel):
    projectSlug: str = None
    milestoneId: str = None
    milestoneIds: list = None
    attributeKey: str = None
