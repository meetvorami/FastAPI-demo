from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.v1.common_utils.auth_utils import get_current_user
from src.api.v1.UserManagement.schemas.schema import LoginUser, ReturnUser
from src.api.v1.UserManagement.services.user_services import UserController

router = APIRouter(prefix="/usermanagement", tags=["User Management"])


@router.post("/create_user")
def create_user(request_data: LoginUser, background_task: BackgroundTasks):
    return UserController().create_user(
        user_object=request_data, background_task=background_task
    )


@router.post("/login")
def login_user(request_data: LoginUser):
    return UserController().login_user(request_data)


@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    return UserController().generate_access_token(refresh_token=refresh_token)


@router.get("/logout")
async def logout(user=Depends(get_current_user)):
    return UserController().logout(user)


@router.get("/list_user", response_model=List[ReturnUser])
async def list_user(user=Depends(get_current_user)):
    return UserController().list_user()
