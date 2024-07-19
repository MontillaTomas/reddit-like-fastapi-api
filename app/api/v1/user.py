"""
Module for defining user-related API routes and operations in version 1 of the API.

This module defines the user_router APIRouter instance for managing user endpoints.
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.user import UserCreate, UserPublic, UserUpdateUsername, UserUpdatePassword
from app.service.user_service import UserService

user_router = APIRouter(prefix="/v1/users", tags=["Users"])


@user_router.get("/{user_id}",
                 response_model=UserPublic,
                 summary="Get a user by ID",
                 response_description="The user with the provided ID.",
                 status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, session: Session = Depends(get_db)):
    """
    Get a user by its ID.

    - **user_id**: ID of the user to retrieve.

    Returns the user with the provided ID.

    Raises HTTPException if the user with the provided ID is not found.
    """
    user_service = UserService(session)
    return user_service.get_by_id(user_id)


@user_router.post("/",
                  response_model=UserPublic,
                  summary="Create a user",
                  response_description="The created user.",
                  status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    """
    Create a new user.

    - **email**: Email address of the user.
    - **username**: Username of the user.
    - **password**: Password of the user.

    Returns the created user.

    Raises HTTPException if the username or email is already registered.
    """
    user_service = UserService(session)
    return user_service.create(user)


@user_router.put("/{user_id}/username",
                 response_model=UserPublic,
                 summary="Update a user's username",
                 response_description="The updated user.",
                 status_code=status.HTTP_200_OK)
def update_user_username(user_id: int, new_username: UserUpdateUsername,
                         session: Session = Depends(get_db)):
    """
    Update a user's username.

    - **user_id**: ID of the user to update.
    - **new_username**: New username for the user.

    Returns the updated user.

    Raises HTTPException if the user with the provided ID is not found or if the username is 
    already registered or if the new username is the same as the old username.
    """
    user_service = UserService(session)
    return user_service.update_username(user_id, new_username)


@user_router.put("/{user_id}/password",
                 response_model=UserPublic,
                 summary="Update a user's password",
                 response_description="The updated user.",
                 status_code=status.HTTP_200_OK)
def update_user_password(user_id: int, user_passwords: UserUpdatePassword,
                         session: Session = Depends(get_db)):
    """
    Update a user's password.

    - **user_id**: ID of the user to update.
    - **user_passwords**: New and old passwords for the user.

    Returns the updated user.

    Raises HTTPException if the user with the provided ID is not found or if the old password is
    incorrect or if the new password is the same as the old password.
    """
    user_service = UserService(session)
    return user_service.update_password(user_id, user_passwords)
