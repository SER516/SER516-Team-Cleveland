import json

from pydantic import BaseModel


class ProjectRequest(BaseModel):
    projectslug: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')
