"""
Module for defining token-related schemas.
"""
from datetime import datetime
from pydantic import BaseModel
from .user import UserPayload


class Token(BaseModel):
    """
    Schema for the token.

    Attributes:
        access_token (str): The JWT access token.
        access_token_type (str): The type of the access token, default is 'Bearer'.
        access_token_expire_time (datetime): The expiration time of the access token.
        user (UserPublic): The user data included in the token.
    """
    access_token: str
    token_type: str = 'Bearer'
    expire_time: datetime
    user: UserPayload


class TokenData(BaseModel):
    """
    Schema for the token data.

    Attributes:
        user (UserPublic): The user data included in the token.
    """
    user: UserPayload
