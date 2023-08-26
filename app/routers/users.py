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
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

user_service = UserService()


@router.get("/")
async def get_users():
    return {"users": "all users"}


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
    response_description="User found",
    response_model=user_models.UserData
)
async def get_a_user(
    username: Annotated[
        str,
        Path(
            title="Username",
            description="The username of the user to get",
            example="Mario64"
        )
    ]
):
    """
    Retrieves information about a user based on their username.

    **Params** 

    - `username [str]`: The `username` path parameter represents the username of the user to get.

    **Returns** 

    - The user information for the specified username.
    """
    user_info = await user_service.get_user(username)
    return user_info


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
