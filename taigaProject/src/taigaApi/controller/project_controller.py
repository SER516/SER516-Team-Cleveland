from fastapi import FastAPI, Request, APIRouter

from taigaApi.auth.authenticate import authenticate
from taigaApi.model.authRequest import AuthRequest

from taigaApi.util.SimpleCache import cache

from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.project.getProjectTaskStatusName import get_project_task_status_name

router = APIRouter()

@router.get("/Project/{project_slug}")
def auth(project_slug: str):
    token = cache.get("token")
    project_info = get_project_by_slug(project_slug, token)
    task_status_name = get_project_task_status_name(project_info["id"], token)

    project_details = {
        "name": project_info["name"],
        "team_members": [member["full_name"] for member in project_info.get("members", [])],
        "taskboard_column": [status["name"] for status in task_status_name],
    }
    return project_details





