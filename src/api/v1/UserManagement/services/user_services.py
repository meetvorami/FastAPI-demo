import json
from datetime import datetime,timezone

from fastapi import HTTPException, status
from passlib.context import CryptContext

from database.database import get_db
from src.api.v1.UserManagement.utils.redis_utils import RedisClient
from src.api.v1.UserManagement.models.models import Users
from src.api.v1.UserManagement.schemas.schema import LoginUser
from src.api.v1.UserManagement.utils.jwt_utils import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class UserController:
    def __init__(self):
        self.db = next(get_db())
        self.redis_client = RedisClient()
        self.tokens = Token()

    def create_user(self, user_object: LoginUser):
        check_user = Users.get_user_by_username(db_session=self.db,username=user_object.username)
        if check_user:
            return HTTPException(status_code=400, detail="Username already exist")
        hashed_password = get_password_hash(user_object.password)
        _, db_user= Users.create_user(self.db,{"username":user_object.username,"password":hashed_password})
        return db_user

    def login_user(self, user_object: LoginUser):
        user = Users.get_user_by_username(self.db,user_object.username)
        if not user:
            return False
        if not pwd_context.verify(user_object.password, user.password):
            return False

        
        access_token = self.tokens.create_access_token(
            data={"sub": user.username, "is_active": user.isactive}
        )
        
        refresh_token = self.tokens.create_refresh_token(
            data={"sub": user.username, "is_active": user.isactive}
        )
        
        self.redis_client.set(
            user.username,
            json.dumps({"access": access_token, "refresh": refresh_token}),
            self.tokens.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    
    def list_user(self):
        return Users.get_all_user(self.db)
    
    
    def generate_access_token(self,refresh_token):
        payload = self.tokens.decode_jwt(refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        tokens = self.redis_client.get(username)
        if tokens is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        tokens = json.loads(tokens)

        if tokens["refresh"] != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        expiration = payload.get("exp")
        if expiration is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has no expiration",
            )
        expiration_datetime = datetime.fromtimestamp(expiration, tz=timezone.utc)
        if datetime.now(timezone.utc) > expiration_datetime:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )

        access_token = self.tokens.create_access_token(
            data={"sub": username, "is_active": payload.get("is_active")}
        )
        self.redis_client.set(username,json.dumps({"access": access_token, "refresh": refresh_token}),self.tokens.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        return {"access": access_token}

    
    def logout(self,user):
        self.redis_client.delete(user.username)
        return {"message": "user logout successfully"}
