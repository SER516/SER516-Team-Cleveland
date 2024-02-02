from fastapi import FastAPI, Request, APIRouter, HTTPException

from taigaApi.auth.authenticate import authenticate
from taigaApi.model.authRequest import AuthRequest

from taigaApi.util.SimpleCache import cache

router = APIRouter()

@router.get("/auth")
def auth(auth: AuthRequest):
    token = authenticate(auth.username, auth.password)
    if token == None:
        raise HTTPException(status_code=404, detail="Invalid Login Credentials")
    cache.set("token", token)
    return {"auth_token": token}




