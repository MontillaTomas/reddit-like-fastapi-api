"""
This module define the UserService class responsible for handling business logic
related to user entities.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schema.user import UserCreate, UserPublic, UserUpdateUsername, UserUpdatePassword, UserDelete
from app.crud.crud_user import CRUDUser
from app.core.pw_utils import hash_password, verify_password


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
                status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

        if self.crud.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Hash the password before storing it
        user.password = hash_password(user.password)
        # Create the user
        return self.crud.create(user)

    def get_by_id(self, user_id: int) -> UserPublic:
        """
        Gets a user by its ID.

        Args:
            user_id (int): ID of the user to retrieve.

        Returns:
            UserPublic: User entity object if found.

        Raises:
            HTTPException: If the user with the given ID is not found.
        """
        user = self.crud.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id={user_id} was not found")

        profile_picture = self.crud.get_current_profile_picture(user_id)

        return UserPublic(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            profile_picture=profile_picture
        )

    def update_username(self, user_id: int, new_username: UserUpdateUsername) -> UserPublic:
        """
        Updates the username of a user.

        Args:
            user_id (int): ID of the user to update.
            new_username (UserUpdateUsername): UserUpdateUsername schema instance containing the 
            new username.

        Returns:
            UserPublic: Updated User entity object.

        Raises:
            HTTPException: If the user with the given ID is not found or the new username is
            already registered or the new username is the same as the old username.
        """
        user = self.crud.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id={user_id} was not found")

        if user.username == new_username.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="New username is the same as the old username"
            )

        if self.crud.get_by_username(new_username.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
            )

        user.username = new_username.username
        return self.crud.update(user)

    def update_password(self, user_id: int, password_schema: UserUpdatePassword) -> UserPublic:
        """
        Updates the password of a user.

        Args:
            user_id (int): ID of the user to update.
            password_schema (UserUpdatePassword): UserUpdatePassword schema instance containing the 
            old and new passwords.

        Returns:
            UserPublic: Updated User entity object.

        Raises:
            HTTPException: If the user with the given ID is not found or the old password is 
            incorrect or the new password is the same as the old password
        """
        user = self.crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id={user_id} was not found")

        if not verify_password(password_schema.old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Old password is incorrect"
            )

        if password_schema.old_password == password_schema.new_password:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="New password cannot be the same as the old password"
            )

        user.password = hash_password(password_schema.new_password)
        return self.crud.update(user)

    def delete(self, user_id: int, password: UserDelete) -> None:
        """
        Deletes a user.

        Args:
            user_id (int): ID of the user to delete.
            password (UserDelete): UserDelete schema instance containing the user's password.

        Raises:
            HTTPException: If the user with the given ID is not found or the password is incorrect.
        """
        user = self.crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id={user_id} was not found")

        if not verify_password(password.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is incorrect"
            )

        self.crud.delete(user)
