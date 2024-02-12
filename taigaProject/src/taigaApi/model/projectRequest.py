from pydantic import BaseModel

class ProjectRequest(BaseModel):
    projectslug: str