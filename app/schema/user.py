"""
Module defining user-related schemas.

This module contains Pydantic models related to user management, including
input data models for creating users, and output data models for returning
user information.
"""

from pydantic import BaseModel, EmailStr
from .base_schema import BaseSchema


class UserBase(BaseModel):
    """
    Base schema for user.

    Attributes:
        email (EmailStr): Email address of the user.
        username (str): Username of the user.
    """
    email: EmailStr
    username: str


class UserIn(UserBase):
    """	
    Schema for creating a new user.

    Attributes:
        password (str): Password of the user.
    """
    password: str


class UserOut(UserBase, BaseSchema):
    """
    Schema for returning user information.

    Attributes:
        id (int): The primary key of the user.
    """
    id: int

    model_config = {
        "from_attributes": "true"
    }
