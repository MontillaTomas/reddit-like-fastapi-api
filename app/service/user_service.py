"""
This module define the UserService class responsible for handling business logic
related to user entities.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schema.user import UserCreate, UserPublic
from app.crud.crud_user import CRUDUser
from app.core.security import hash_password


class UserService:
    """
    Service class for managing user-related operations.

    Attributes:
        crud (CRUDUser): Instance of CRUD operations for User entities.
    """

    def __init__(self, session: Session):
        self.crud = CRUDUser(session)

    def create(self, user: UserCreate) -> UserPublic:
        """
        Creates a new user if the username and email are not already registered.

        Args:
            user (UserCreate): UserCreate schema instance containing user data.

        Returns:
            UserPublic: Created User entity object.

        Raises:
            HTTPException: If the username or email is already registered.
        """
        if self.crud.get_by_username(user.username):
            raise HTTPException(
                status_code=400, detail="Username already registered")

        if self.crud.get_by_email(user.email):
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Hash the password before storing it
        user.password = hash_password(user.password)
        # Create the user
        return self.crud.create(user)
