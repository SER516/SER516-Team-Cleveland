from pydantic import BaseModel

class CruftRequest(BaseModel):
    projectSlug: str = None
    startDate: str = None
    endDate: str = None
    attributeKey: str = None