import json

from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')
