from fastapi import APIRouter, HTTPException, Header
from typing import Annotated

from ..model.projectRequest import ProjectRequest

from ..project.getProjectBySlug import get_project_by_slug
from ..util.SimpleCache import cache

from ..util.sprint_service import (
    get_sprints_and_custom_fields_for_project
)

router = APIRouter()


@router.post("/Sprints")
def get_sprint_and_custom_field_details(
    projectRequest: ProjectRequest,
    token: Annotated[str | None, Header()] = None
):
    if cache.get(projectRequest.projectslug) is None:
        project_info = get_project_by_slug(projectRequest.projectslug, token)
        if project_info is None:
            raise HTTPException(
                status_code=404, detail="Project Slug Not Found."
            )
        cache.set(projectRequest.projectslug, project_info)
        return get_sprints_and_custom_fields_for_project(project_info)
    return get_sprints_and_custom_fields_for_project(
        cache.get(projectRequest.projectslug)
    )
