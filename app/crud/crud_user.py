"""
Module for CRUD operations related to users in the database.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.schema.user import UserCreate, UserPublic
from app.model.user import User


class CRUDUser:
    """
    This class encapsulates methods to perform CRUD operations on User entities
    in the database.

    Attributes:
        session (Session): SQLAlchemy database session.
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserCreate):
        """
        Creates a new user record in the database.

        Args:
            user (UserCreate): UserCreate schema instance containing user data.

        Returns:
            User: Created User entity object.
        """
        user = User(**user.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int):
        """
        Retrieves a user record from the database by its ID.

        Args:
            id (int): ID of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str):
        """
        Retrieves a user record from the database by its username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        """
        Retrieves a user record from the database by its email.

        Args:
            email (str): Email of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.email == email).first()

    def update(self, user: UserPublic):
        """
        Updates a user record in the database.

        Args:
            user (UserPublic): UserPublic schema instance containing updated user data.

        Returns:
            UserPublic: Updated User entity object.
        """
        # pylint: disable=not-callable
        user.updated_at = func.now()
        self.session.commit()
        self.session.refresh(user)
        return user
