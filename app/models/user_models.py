"""
User models
"""

from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, SecretStr


class User(BaseModel):
    username: str = Field(
        ...,
        title="Username",
        description="The username of the user",
        min_length=3
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="The email of the user"
    )


class UserPassword(User):
    password: SecretStr = Field(
        ...,
        title="Password",
        description="The password of the user",
        min_length=8
    )


class UserID(UserPassword):
    user_id: UUID
