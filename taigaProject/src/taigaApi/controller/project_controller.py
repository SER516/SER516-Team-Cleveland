from fastapi import APIRouter, HTTPException, Header
from typing import Annotated

from ..model.projectRequest import ProjectRequest

from ..project.getProjectBySlug import get_project_by_slug
from ..util.project_service import get_project_members

router = APIRouter()


@router.post("/Project")
def auth(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    project_info = get_project_by_slug(projectRequest.projectslug, token)
    if project_info is None:
        raise HTTPException(status_code=404, detail="Project Slug Not Found.")

    project_details = {
        "id": project_info["id"],
        "name": project_info["name"],
        "members": get_project_members(project_info)
    }
    return project_details
