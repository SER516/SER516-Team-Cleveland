from pydantic import BaseModel

class CruftRequest(BaseModel):
    projectId: str = None
    startDate: str = None
    endDate: str = None
    attributeKey: str = None