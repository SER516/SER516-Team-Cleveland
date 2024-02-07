from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taigaApi.controller import project_controller
from taigaApi.controller import auth_controller

app = FastAPI()
app.include_router(project_controller.router)
app.include_router(auth_controller.router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You might want to restrict this to specific HTTP methods
    allow_headers=["*"],  # You might want to restrict this to specific headers
)