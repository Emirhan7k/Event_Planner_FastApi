from fastapi import Depends, Header, HTTPException, status


def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    if not authorization:
        return 1
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    return 1
