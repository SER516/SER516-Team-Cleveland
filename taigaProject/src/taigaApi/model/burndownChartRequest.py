from pydantic import BaseModel

class BurndownChartRequest(BaseModel):
    projectSlug: str = None
    milestoneId: str = None
    attributeKey: str = None