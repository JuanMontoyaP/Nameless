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

    def __init__(self):
        self.dynamodb = DynamoDB()
        self.table_name = os.getenv("DB_TABLE_NAME")

    def __check_db(self):
        if not self.dynamodb.check_if_table_exists(self.table_name):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Table {self.table_name} not found"
            )

    async def create_user(self, user: user_models.UserPassword) -> user_models.User:
        """
        Create a user
        """
        new_user = user_models.UserID(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password.get_secret_value()),
            user_id=uuid.uuid4()
        )

        self.__check_db()

        await self.dynamodb.create_item(new_user)

        created_user = await self.dynamodb.get_item_info(
            ["user_id", "username"],
            [str(new_user.user_id), new_user.username],
        )

        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not created"
            )

        return new_user
