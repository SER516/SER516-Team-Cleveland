import json

from pydantic import BaseModel


class CruftRequest(BaseModel):
    projectId: str = None
    startDate: str = None
    endDate: str = None
    attributeKey: str = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')
