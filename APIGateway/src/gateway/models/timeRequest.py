import json

from pydantic import BaseModel


class TimeRequest(BaseModel):
    projectslug: str
    from_date: str = None
    to_date: str = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
