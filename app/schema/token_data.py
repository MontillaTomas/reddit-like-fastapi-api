"""
Module for defining token-related schemas.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for the token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for the token data.
    """
    id: int | None = None
