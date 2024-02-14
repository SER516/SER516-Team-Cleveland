from fastapi import FastAPI, Request, APIRouter, HTTPException, Header
from typing import Annotated

from taigaApi.model.projectRequest import ProjectRequest

from taigaApi.project.getProjectBySlug import get_project_by_slug

router = APIRouter()

@router.post("/Sprints")
def get_sprints_and_custom_fields_for_project(projectRequest: ProjectRequest, token: Annotated[str | None, Header()] = None):
    project_info = get_project_by_slug(projectRequest.projectslug, token)
    if project_info is None:
        raise HTTPException(status_code=404, detail="Project Slug Not Found.")
    custom_attributes = []
    for custom_attribute in project_info["userstory_custom_attributes"]:
        custom_attributes.append({"id": custom_attribute["id"], "name": custom_attribute["name"]})
    sprints = []
    for sprint in project_info["milestones"]:
        sprints.append({"id": sprint["id"], "name": sprint["name"], "slug": sprint["slug"]})

    sprint_details = {
        "sprints": sprints,
        "custom_attributes": custom_attributes,
    }
    return sprint_details





