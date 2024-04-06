import json

from pydantic import BaseModel
from typing import Optional


class DevFocusRequest(BaseModel):
    project_id: str
    members: Optional[list] = None
    from_date: str
    to_date: str
    threshold: str = 2

    def custom_serializer(self, obj):
        return {
            key: value
            for key, value in obj.__dict__.items()
            if value is not None
        }

    def toJSON(self):
        return json.dumps(self, default=lambda obj: self.custom_serializer(obj), skipkeys=True,
                          sort_keys=True, indent=4).encode('utf8')
