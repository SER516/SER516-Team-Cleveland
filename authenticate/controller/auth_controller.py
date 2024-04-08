from fastapi import APIRouter, HTTPException

from auth.authenticate import authenticate
from model.authRequest import AuthRequest

router = APIRouter()


@router.post("/auth")
def auth(auth: AuthRequest):
    token = authenticate(auth.username, auth.password)
    if token is None:
        raise HTTPException(
            status_code=401, detail="Invalid Login Credentials"
        )

    return {"auth_token": token}
