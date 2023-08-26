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

    async def check_user_exist(self, user: user_models.User) -> bool:
        """
        The method `check_user_exist` checks if a user already exists in the database based on their
        username or email.

        Param 
            - user User: The "user" parameter is an instance of the "User" class It represents
                a user object with properties such as "username" and "email"

        Return: 
            - A boolean value. If there are any users found with the same username or email as the
                provided user, it will return True. Otherwise, it will return False.
        """
        users_by_username = await self.dynamodb.scan_item("username", user.username)
        users_by_email = await self.dynamodb.scan_item("username", user.username)

        if users_by_username or users_by_email:
            return True

        return False

    async def create_user(self, user: user_models.UserPassword) -> user_models.User:
        """
        Create a user
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

        user_exist = await self.check_user_exist(new_user)

        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
            )
        await self.dynamodb.create_item(new_user)

        return new_user
