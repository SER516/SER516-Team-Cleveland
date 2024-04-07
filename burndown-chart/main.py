from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import burndown_controller

app = FastAPI()
app.include_router(burndown_controller.router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)