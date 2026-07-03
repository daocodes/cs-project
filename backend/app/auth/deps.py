from fastapi import Header, HTTPException

from app.auth.factory import get_auth_verifier
from app.auth.types import CurrentUser


def get_current_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    try:
        verifier = get_auth_verifier()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    user = verifier.resolve_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
