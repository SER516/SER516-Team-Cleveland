from fastapi import FastAPI

from taigaProject.src.taigaApi.controller import project_controller, \
    auth_controller, metric_controller, sprint_controller

app = FastAPI()
app.include_router(project_controller.router)
app.include_router(auth_controller.router)
app.include_router(metric_controller.router)
app.include_router(sprint_controller.router)
