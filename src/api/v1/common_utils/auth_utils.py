import json
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from database.database import get_db
from src.api.v1.UserManagement.models.models import Users

from ..UserManagement.utils.jwt_utils import Token
from ..UserManagement.utils.redis_utils import RedisClient


def get_current_user(token: str = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = Token().decode_jwt(token.credentials)
        username = payload.get("sub")

    except InvalidTokenError:
        raise credentials_exception
    expiration = payload.get("exp")
    if expiration is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has no expiration"
        )
    expiration_datetime = datetime.fromtimestamp(expiration, tz=timezone.utc)
    if datetime.now(timezone.utc) > expiration_datetime:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    get_user_token = RedisClient().get(username)

    if not get_user_token:
        raise credentials_exception

    tokens = json.loads(get_user_token)

    if tokens["access"] != token.credentials:
        raise credentials_exception

    user = Users.get_user_by_username(db, username)
    return user
