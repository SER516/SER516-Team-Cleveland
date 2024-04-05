import json

from pydantic import BaseModel


class BurndownChartRequest(BaseModel):
    projectSlug: str = None
    milestoneId: str = None
    milestoneIds: list = None
    attributeKey: str = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
