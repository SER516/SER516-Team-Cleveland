from pydantic import BaseModel

class TimeRequest(BaseModel):
    projectslug: str
    from_date: str = None
    to_date: str = None