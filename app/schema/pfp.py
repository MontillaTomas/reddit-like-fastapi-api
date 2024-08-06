"""
Module defining profile picture-related schemas.

This module contains Pydantic models related to profile picture management.
"""

from datetime import datetime
from pydantic import BaseModel, UUID4


class ProfilePictureBase(BaseModel):
    """
    Base schema for ProfilePicture.

    Attributes:
        id (UUID4): The unique identifier for the profile picture.
        user_id (int): The ID of the user associated with the profile picture.
        path (str): The file path of the profile picture.
    """
    id: UUID4
    user_id: int
    path: str


class ProfilePictureCreate(ProfilePictureBase):
    """
    Schema for creating a new profile picture.

    Inherits all attributes from ProfilePictureBase.

    Attributes:
        id (UUID4): The unique identifier for the profile picture.
        user_id (int): The ID of the user associated with the profile picture.
        path (str): The file path of the profile picture.
    """


class ProfilePicturePublic(ProfilePictureBase):
    """
    Public schema for ProfilePicture.

    Attributes:
        id (UUID4): The unique identifier for the profile picture.
        user_id (int): The ID of the user associated with the profile picture.
        path (str): The file path of the profile picture.
        uploaded_at (datetime): The timestamp when the profile picture was uploaded.
    """
    uploaded_at: datetime

    model_config = {
        "from_attributes": "true"
    }
