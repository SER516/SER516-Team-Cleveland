from fastapi import APIRouter, HTTPException

from ..auth.authenticate import authenticate
from ..model.authRequest import AuthRequest

from ..util.SimpleCache import cache

router = APIRouter()


@router.post("/auth")
def auth(auth: AuthRequest):
    token = authenticate(auth.username, auth.password)
    if token is None:
        raise HTTPException(
            status_code=401, detail="Invalid Login Credentials"
        )

    cache.set("token", token)
    return {"auth_token": token}
