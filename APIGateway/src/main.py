import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.controllers import project_controller, sprint_controller
from gateway.controllers import metric_controller, auth_controller

app = FastAPI()
app.include_router(project_controller.router)
app.include_router(auth_controller.router)
app.include_router(metric_controller.router)
app.include_router(sprint_controller.router)

origins = ["http://localhost:3000"]
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT')))
