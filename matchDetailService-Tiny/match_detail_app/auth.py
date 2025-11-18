"""Simple authentication helpers supporting JWT or API Key headers."""
from typing import Optional

import jwt
from fastapi import Header, HTTPException, status

from .config import settings


def require_auth(
    authorization: Optional[str] = Header(default=None),
    api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    """Accept either a Bearer JWT or an API key header."""

    if api_key and api_key in settings.api_keys:
        return {"method": "api-key", "subject": "api-key"}

    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token:
            try:
                payload = jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[settings.jwt_algorithm],
                )
                return {"method": "jwt", "subject": payload.get("sub"), "claims": payload}
            except jwt.PyJWTError as exc:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
