from datetime import datetime,timezone
from src.api.v1.UserManagement.utils.redis_utils import RedisClient
import json 
from src.api.v1.UserManagement.models.models import Users
from src.api.v1.UserManagement.utils.jwt_utils import Token
from database.database import get_db

class GetCurrentUser:
    def __init__(self) -> None:
        self.db = next(get_db())
    
    async def get_user(self,token):
        try:
            payload = Token().decode_jwt(token)
            username = payload.get("sub")
        except Exception as e:
            print(f"Error in the code: {e}")
            return False
        
        expiration = payload.get("exp")
        if expiration is None:
            return False
        expiration_datetime = datetime.fromtimestamp(expiration, tz=timezone.utc)
        if datetime.now(timezone.utc) > expiration_datetime:
            return False

        get_user_token = RedisClient().get(username)

        if not get_user_token:
            return False

        tokens = json.loads(get_user_token)

        if tokens["access"] != token:
            return False

        user=  Users.get_user_by_username(self.db, username) 
        return user
        