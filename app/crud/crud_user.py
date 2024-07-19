"""
Module for CRUD operations related to users in the database.
"""

from sqlalchemy.orm import Session
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

    def create(self, user: UserCreate) -> UserPublic:
        """
        Creates a new user record in the database.

        Args:
            user (UserCreate): UserCreate schema instance containing user data.

        Returns:
            UserPublic: Created User entity object.
        """
        user = User(**user.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> UserPublic:
        """
        Retrieves a user record from the database by its ID.

        Args:
            id (int): ID of the user to retrieve.

        Returns:
            UserPublic: User entity object if found, None otherwise.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> UserPublic:
        """
        Retrieves a user record from the database by its username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            UserPublic: User entity object if found, None otherwise.
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> UserPublic:
        """
        Retrieves a user record from the database by its email.

        Args:
            email (str): Email of the user to retrieve.

        Returns:
            UserPublic: User entity object if found, None otherwise.
        """
        return self.session.query(User).filter(User.email == email).first()
