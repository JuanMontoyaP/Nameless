"""
User models
"""

from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, SecretStr


class User(BaseModel):
    """
    This is the base class for all the user models.
    """
    username: str = Field(
        ...,
        title="Username",
        description="The username of the user",
        min_length=3,
        examples=["Mario64"]
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="The email of the user",
        examples=["mario64@example.com"]
    )


class UserPassword(User):
    """
    This is class inherited from User base class and adds a password to the user. 
    """
    password: SecretStr = Field(
        ...,
        title="Password",
        description="The password of the user",
        min_length=8,
        examples=["password123"]
    )


class UserData(UserPassword):
    """
    This class contains all the user data.
    """
    first_name: str = Field(
        ...,
        title="First name",
        description="The first name of the user",
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z]*$",
        examples=["Mario"]
    )
    last_name: str = Field(
        ...,
        title="Last name",
        description="The last name of the user",
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z]*$",
        examples=["Bros"]
    )
    age: int = Field(
        ...,
        title="Age",
        description="The age of the user",
        gt=0,
        lt=150,
        examples=[25]
    )


class UserID(UserData):
    """
    Adds the user ID to the user data.
    """
    user_id: UUID
    password: str
