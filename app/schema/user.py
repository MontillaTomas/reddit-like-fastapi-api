"""
Module defining user-related schemas.

This module contains Pydantic models related to user management, including
input data models for creating users, and output data models for returning
user information.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.core.pw_validator import validate_password
from .base_schema import BaseSchema
from .pfp import ProfilePicturePublic


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
        email (EmailStr): Email address of the user.
        username (str): Username of the user.
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
        return validate_password(value)


class UserPublic(UserBase, BaseSchema):
    """
    Schema for returning user information.

    Attributes:
        id (int): The primary key of the user.
        email (EmailStr): Email address of the user.
        username (str): Username of the user.
        created_at (datetime): Timestamp indicating creation time.
        updated_at (datetime, optional): Timestamp indicating last update time.
        profile_picture (ProfilePicturePublic, optional): Profile picture of the user.
    """
    id: int
    profile_picture: ProfilePicturePublic | None = None

    model_config = {
        "from_attributes": "true"
    }


class UserUpdateUsername(BaseModel):
    """
    Schema for updating a user's username.

    Attributes:
        username (str): The new username for the user.
    """
    username: str


class UserUpdatePassword(BaseModel):
    """
    Schema for updating a user's password.

    Attributes:
        old_password (str): The user's current password.
        new_password (str): The new password for the user.
    """
    old_password: str
    new_password: str = Field(min_length=8, max_length=30)

    @field_validator("new_password")
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
        return validate_password(value)


class UserDelete(BaseModel):
    """
    Schema for deleting a user.

    Attributes:
        password (str): The user's password.
    """
    password: str


class UserPayload(BaseModel):
    """
    Schema for user payload for JWT token.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user.
    """
    id: int
    username: str
