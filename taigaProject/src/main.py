import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taigaApi.controller import project_controller
from taigaApi.controller import auth_controller
from taigaApi.controller import metric_controller
from taigaApi.controller import sprint_controller

app = FastAPI()
app.include_router(project_controller.router)
app.include_router(auth_controller.router)
app.include_router(metric_controller.router)
app.include_router(sprint_controller.router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT')))
