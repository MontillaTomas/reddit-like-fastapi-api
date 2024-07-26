"""
Module for CRUD operations related to users in the database.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.schema.user import UserCreate
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

    def create(self, user: UserCreate) -> User:
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

    def get_by_id(self, user_id: int) -> User:
        """
        Retrieves a user record from the database by its ID.

        Args:
            id (int): ID of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User:
        """
        Retrieves a user record from the database by its username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        """
        Retrieves a user record from the database by its email.

        Args:
            email (str): Email of the user to retrieve.

        Returns:
            User: User entity object if found.
        """
        return self.session.query(User).filter(User.email == email).first()

    def update(self, user: User) -> User:
        """
        Updates a user record in the database.

        Args:
            user (UserPublic): UserPublic schema instance containing updated user data.

        Returns:
            UserPublic: Updated User entity object.
        """
        user.updated_at = func.now()  # pylint: disable=not-callable
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """
        Deletes a user record from the database.

        Args:
            user (User): User entity object to delete.
        """
        self.session.delete(user)
        self.session.commit()
