from pydantic import BaseModel

class ProjectRequest(BaseModel):
    authtoken: str
    projectslug: str