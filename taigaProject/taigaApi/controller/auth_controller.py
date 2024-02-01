from fastapi import FastAPI, Request, APIRouter

from taigaApi.auth.authenticate import authenticate
from taigaApi.model.authRequest import AuthRequest

from taigaApi.util.SimpleCache import cache

router = APIRouter()

@router.get("/auth")
def auth(auth: AuthRequest):
    token = authenticate(auth.username, auth.password)
    cache.set("token", token)
    return {"auth_token": token}




