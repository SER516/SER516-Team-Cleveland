from fastapi import APIRouter, HTTPException, Header
from typing import Annotated

from taigaApi.model.projectRequest import ProjectRequest

from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.project.getProjectTaskStatusName import (
    get_project_task_status_name
)

router = APIRouter()


@router.post("/Project")
def auth(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    project_info = get_project_by_slug(projectRequest.projectslug, token)
    if project_info is None:
        raise HTTPException(status_code=404, detail="Project Slug Not Found.")
    task_status_name = get_project_task_status_name(project_info["id"], token)

    project_details = {
        "name": project_info["name"],
        "team_members": [
            member["full_name"] for member in project_info.get("members", [])
        ],
        "taskboard_column": [
            status["name"] for status in task_status_name
        ],
    }
    return project_details
