from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import lead_time_controller

app = FastAPI()
app.include_router(lead_time_controller.router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
