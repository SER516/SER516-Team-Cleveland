import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import requests

from ..models.authRequest import AuthRequest

router = APIRouter()
load_dotenv()

@router.post("/auth")
def auth(auth: AuthRequest):
    auth_url = os.getenv('AUTH_URL')
    try:
        response = requests.post(f"{auth_url}/auth", data=auth.toJSON())
        response.raise_for_status()
        return response.json()

    except (HTTPException, requests.exceptions.RequestException) as e:
        print(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=401, detail="Invalid Login Credentials"
        )
