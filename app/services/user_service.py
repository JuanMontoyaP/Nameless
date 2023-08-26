"""
User service class
"""

import os
import uuid
from dotenv import load_dotenv

from fastapi import HTTPException, status

from ..models import user_models
from ..db.dynamo_db import DynamoDB
from ..utils.passwords import get_password_hash

load_dotenv()


class UserService:
    """
    User service class for all the logic methods of users
    """

    def __init__(self):
        self.dynamodb = DynamoDB()
        self.table_name = os.getenv("DB_TABLE_NAME")

    def __check_db(self):
        if not self.dynamodb.check_if_table_exists(self.table_name):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Table {self.table_name} not found"
            )

    async def check_user_exist(self, user_data: str, user_identifier: str = "username") -> bool:
        """
        The method `check_user_exist` checks if a user already exists in the database based on their
        username or email.

        Params
            - username str: The "user" parameter is an instance of the "User" class It represents
                a user object with properties such as "username" and "email"
            - email str: 

        Return: 
            - A boolean value. If there are any users found with the same username or email as the
                provided user, it will return True. Otherwise, it will return False.
        """
        users = await self.dynamodb.scan_item(user_identifier, user_data)

        if users:
            return True

        return False

    async def create_user(self, user: user_models.UserPassword) -> user_models.User:
        """
        The `create_user` method creates a new user in a database, checking if the username or email
        already exist before creating the user.

        Params 
            - user UserPassword: The `user` parameter is an instance of the `UserPassword` model.

        Returns 
            - A new user object of type `User` of the created user.
        """
        new_user = user_models.UserID(
            user_id=uuid.uuid4(),
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password.get_secret_value()),
            first_name=user.first_name,
            last_name=user.last_name,
            age=user.age
        )

        self.__check_db()

        user_exist = await self.check_user_exist(new_user.username)
        email_exist = await self.check_user_exist(new_user.email, "email")

        if user_exist or email_exist:
            msg = "Username already exist" if user_exist else "Email already exist"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=msg
            )
        await self.dynamodb.create_item(new_user)

        return new_user

    async def get_user(self, username: str) -> user_models.UserInfo:
        """
        The method `get_user` retrieves user data from a database based on a given username and 
        returns it as an instance of the `UserData` class.

        Params 
            - username str: The `username` parameter is a string that represents the username of the 
                user we want to retrieve from the database

        Returns 
            - An instance of the `user_models.UserData` class.
        """
        self.__check_db()

        user = await self.dynamodb.get_item_info(
            ["username"],
            [username],
            [
                "username",
                "email",
                "first_name",
                "last_name",
                "age"
            ]
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist"
            )

        return user_models.UserInfo(**user)

    async def update_user(self, username: str, new_data: user_models.UserInfo):
        """
        The `update_user` method updates the user information in the database with the provided 
        new data.

        Params
            - username str: The username parameter is a string that represents the username of the
                user whose information needs to be updated
            - new_data UserInfo: It contains the updated information for a user, including the 
                email, first name, last name, and age

        Returns 
            - An instance of the `UserInfo` class with the updated user information.
        """

        self.__check_db()
        updated_user = await self.dynamodb.update_item(
            {'username': username},
            "Set email = :email, first_name = :first_name, last_name = :last_name, age = :age",
            {
                ':email': new_data.email,
                ':first_name': new_data.first_name,
                ':last_name': new_data.last_name,
                ':age': new_data.age
            }
        )

        return user_models.UserInfo(username=username, **updated_user)
