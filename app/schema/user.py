"""
Module defining user-related schemas.

This module contains Pydantic models related to user management, including
input data models for creating users, and output data models for returning
user information.
"""
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
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


class UserCreate(UserBase):
    """	
    Schema for creating a new user.

    Attributes:
        password (str): Password of the user. The password must be between 8 and 30 characters long.
        It must contain at least one uppercase letter, one lowercase letter, one digit, and one 
        special character from the set [@#$%^&+=-].
    """
    password: str = Field(min_length=8, max_length=30)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        """
        Validate the password.

        Args:
            value (str): The password to be validated.

        Raises:
            ValueError: If the password does not meet the required criteria.

        Returns:
            str: The validated password.
        """

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@#$%^&+=-]", value):
            raise ValueError(
                "Password must contain at least one special character from [@#$%^&+=-]")
        return value


class UserPublic(UserBase, BaseSchema):
    """
    Schema for returning user information.

    Attributes:
        id (int): The primary key of the user.
    """
    id: int

    model_config = {
        "from_attributes": "true"
    }
