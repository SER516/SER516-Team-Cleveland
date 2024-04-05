import json

from pydantic import BaseModel
from typing import Optional


class DevFocusRequest(BaseModel):
    project_id: str
    members: Optional[list] = None
    from_date: str
    to_date: str
    threshold: str = 2

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')
