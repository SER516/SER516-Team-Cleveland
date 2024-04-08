import json

from pydantic import BaseModel


class TimeRequest(BaseModel):
    projectslug: str
    from_date: str = None
    to_date: str = None

    def custom_serializer(self, obj):
        return {
            key: value
            for key, value in obj.__dict__.items()
            if value is not None
        }

    def toJSON(self):
        return json.dumps(self,
                          default=lambda obj: self.custom_serializer(obj),
                          skipkeys=True,
                          sort_keys=True, indent=4).encode('utf8')
