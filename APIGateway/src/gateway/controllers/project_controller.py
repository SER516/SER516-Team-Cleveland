import os

from dotenv import load_dotenv
from fastapi import APIRouter, Header
from typing import Annotated

from ..models.projectRequest import ProjectRequest
from ..util.http_requests_util import post_call

router = APIRouter()
load_dotenv()


@router.post("/Project")
def auth(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    project_url = os.getenv('PROJECT_INFO_URL')
    return post_call(project_url, token, projectRequest, 'Project')
