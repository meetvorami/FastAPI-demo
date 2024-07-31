from fastapi import APIRouter, Depends

from src.api.v1.common_utils.auth_utils import get_current_user
from src.api.v1.UserManagement.services.user_services import UserController
from src.api.v1.UserManagement.schemas.schema import LoginUser, ReturnUser
from typing import List

router = APIRouter(prefix="/usermanagement",tags=["User Management"])


@router.post("/create_user")
def create_user(request_data: LoginUser):
    user = UserController().create_user(user_object=request_data)
    return user


@router.post("/login")
def login_user(request_data: LoginUser):
    data = UserController().login_user(request_data)
    return data


@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    data = UserController().generate_access_token(refresh_token=refresh_token)
    return data


@router.get("/logout")
async def logout(user=Depends(get_current_user)):
    data = UserController().logout(user)
    return data


@router.get("/list_user", response_model=List[ReturnUser])
async def list_user(user=Depends(get_current_user)):
    data = UserController().list_user()
    return data
