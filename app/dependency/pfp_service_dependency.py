"""
This module provides a dependency function for getting a ProfilePictureService instance.
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.service.pfp_service import ProfilePictureService


def get_pfp_service(session: Annotated[Session, Depends(get_db)]):
    """
    Provides a ProfilePictureService instance with the provided session.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        ProfilePictureService: The ProfilePictureService instance
    """
    return ProfilePictureService(session)
