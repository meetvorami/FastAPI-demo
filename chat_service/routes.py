from fastapi import APIRouter , WebSocket, Depends
from src.api.v1.UserManagement.utils.jwt_utils import Token
from datetime import datetime,timezone
from src.api.v1.UserManagement.utils.redis_utils import RedisClient
import json 
from src.api.v1.UserManagement.models.models import Users
from sqlalchemy.orm import Session
from database.database import get_db

from chat_service.auth_details import GetCurrentUser
from chat_service.userservices import UserServices


router = APIRouter()


@router.websocket("/lobby/")
async def get_user_lobby(websocket: WebSocket,token: str,skip:int= 0, limit:int = 10 ):
    try:
        await websocket.accept()  
        user = await GetCurrentUser().get_user(token)
        print('user: ', user)
        if not user:
            await websocket.send("Invalid token")
            await websocket.close()
        user_services = UserServices()
        room_list  = user_services.check_if_user_part_of_room(user.id)
        if not room_list:
            await websocket.send(f"roomlist : {json.dumps([])}")
        else:
            print("here in else")
            get_latest_message_from_db = user_services.get_latest_message(room_list,skip,limit)
            await websocket.send_text(f"user connected with fastapi: {json.dumps(get_latest_message_from_db)}")
    except Exception as e:
        print('e: ', e)
        await websocket.send_text("User not authorized to join this room.")
        await websocket.close() 
