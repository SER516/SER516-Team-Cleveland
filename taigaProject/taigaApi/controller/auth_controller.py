from fastapi import FastAPI, Request, APIRouter, HTTPException

from taigaApi.auth.authenticate import authenticate
from taigaApi.model.authRequest import AuthRequest

from taigaApi.util.SimpleCache import cache

router = APIRouter()

@router.post("/auth")
def auth(auth: AuthRequest):
    token = authenticate(auth.username, auth.password)
    if token == None:
        raise HTTPException(status_code=401, detail="Invalid Login Credentials")

    cache.set("token", token)
    return {"auth_token": token}
