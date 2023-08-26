"""
This file will handle all the logic related to passwords
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    The function `get_password_hash` takes a password as input and returns its hash value.

    Params 
        - password: The password parameter is the plain text password that you want to hash

    Returns 
        - The hash of the password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    The function `verify_password` takes a plain password and a hashed password as input and returns
    True if the plain password matches the hashed password, and False otherwise.

    Params 
        - plain_password: The plain_password parameter is the password entered by the user in plain 
            text
        - hashed_password: The hashed password parameter is the password stored in the database

    Returns 
        - True if the plain_password matches the hashed_password, and False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
