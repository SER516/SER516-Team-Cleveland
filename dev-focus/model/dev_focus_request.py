from pydantic import BaseModel
from typing import Optional


class DevFocusRequest(BaseModel):
    project_id: str
    members: Optional[list] = None
    from_date: str
    to_date: str
    threshold: str = 2
