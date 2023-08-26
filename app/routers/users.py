"""
This section is handles all the users endpoints.
"""

from typing import Annotated

from fastapi import APIRouter
from fastapi import Path, Body
from fastapi import status

from ..models import user_models
from ..services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

user_service = UserService()


@router.get("/")
async def get_users():
    return {"users": "all users"}


@router.get("/{user_id}")
async def get_a_user(
    user_id: Annotated[int, Path(title="The ID of the user")]
):
    return {"users": user_id}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_description="User has been created",
    response_model=user_models.User,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"}
    },
    summary="Create a new user",
)
async def create_user(
    new_user: Annotated[
        user_models.UserData,
        Body(
            title="User to create",
            description="The user to create"
        )
    ]
):
    """
    Creates a new user with the following information:

    - **username**
    - **email**
    - **password**
    - **first_name**
    - **last_name**
    - **age**

    The password is hashed and stored in the database.
    """
    created_user = await user_service.create_user(new_user)
    return created_user.model_dump()
