from fastapi import FastAPI, Request, APIRouter, HTTPException

from taigaApi.model.projectRequest import ProjectRequest

from taigaApi.project.getProjectBySlug import get_project_by_slug
from taigaApi.project.getProjectTaskStatusName import get_project_task_status_name

router = APIRouter()

@router.get("/Project")
def auth(projectRequest: ProjectRequest):
    project_info = get_project_by_slug(projectRequest.projectslug, projectRequest.authtoken)
    if project_info is None:
        raise HTTPException(status_code=404, detail="Project Slug Not found")
    task_status_name = get_project_task_status_name(project_info["id"], projectRequest.authtoken)

    project_details = {
        "name": project_info["name"],
        "team_members": [member["full_name"] for member in project_info.get("members", [])],
        "taskboard_column": [status["name"] for status in task_status_name],
    }
    return project_details





