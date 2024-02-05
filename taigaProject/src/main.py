from fastapi import FastAPI

from taigaApi.controller import project_controller
from taigaApi.controller import auth_controller

app = FastAPI()
app.include_router(project_controller.router)
app.include_router(auth_controller.router)