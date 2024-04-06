import json

from pydantic import BaseModel


class CruftRequest(BaseModel):
    projectId: str = None
    startDate: str = None
    endDate: str = None
    attributeKey: str = None

    def custom_serializer(self, obj):
        return {
            key: value
            for key, value in obj.__dict__.items()
            if value is not None
        }

    def toJSON(self):
        return json.dumps(self, default=lambda obj: self.custom_serializer(obj), skipkeys=True,
                          sort_keys=True, indent=4).encode('utf8')
