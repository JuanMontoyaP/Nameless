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


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
    response_description="User found",
    response_model=user_models.UserInfo
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

    - `username`
    - `email`
    - `password`
    - `first_name`
    - `last_name`
    - `age`

    The password is hashed and stored in the database.
    """
    created_user = await user_service.create_user(new_user)
    return created_user.model_dump()


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="User has been updated",
    summary="Update a user",
    response_model=user_models.UserInfo
)
async def update_user(
    new_data: Annotated[
        user_models.UserInfo,
        Body(
            title="User to update",
            description="The user to update"
        )
    ]
):
    """
    Updates a user's information using the provided new data.

    **Body Parameter**

    - `new_data` JSON file with the following fields:

        - `username`: username of the user to be updated.
        - `email`: new email of the user to be updated.
        - `first_name`: new first name of the user to be updated.
        - `last_name`: new last name of the user to be updated.
        - `age`: new age of the user to be updated.

        All fields are required and the username is the only field that can not
        be updated.

    **Returns** 

    - The updated user information.
    """
    updated_data = await user_service.update_user(new_data.username, new_data)
    return updated_data


@router.delete(

    "/{username}",
    status_code=status.HTTP_200_OK,
    response_description="User has been deleted",
    response_model=user_models.UserInfo,
    summary="Delete a user"
)
async def delete_user(
    username: Annotated[
        str,
        Path(
            title="Username",
            description="The username of the user to delete",
            example="Mario64",
            min_length=3,
            max_length=50
        )
    ]
):
    """
    Deletes a user with the specified username.

    **Parameters**

    - `username`: The username of the user to be deleted. It is a required parameter.

    **Returns**

    - The deleted user.
    """
    deleted_user = await user_service.delete_user(username)
    return deleted_user
