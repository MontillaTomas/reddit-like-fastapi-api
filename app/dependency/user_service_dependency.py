"""
This module provides a dependency function for getting a UserService instance.
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.service.user_service import UserService


def get_user_service(session: Annotated[Session, Depends(get_db)]):
    """
    Provides a UserService instance with the provided session.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        UserService: The UserService instance
    """
    return UserService(session)
