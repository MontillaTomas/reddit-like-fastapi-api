"""
Module for defining user-related API routes and operations in version 1 of the API.

This module defines the user_router APIRouter instance for managing user endpoints.
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.user import UserCreate, UserPublic
from app.service.user_service import UserService

user_router = APIRouter(prefix="/v1/users", tags=["Users"])


@user_router.get("/{user_id}", response_model=UserPublic, summary="Get a user by ID",
                 response_description="The user with the provided ID.")
def get_user_by_id(user_id: int, session: Session = Depends(get_db)):
    """
    Get a user by its ID.

    - **user_id**: ID of the user to retrieve.

    Returns the user with the provided ID.

    Raises HTTPException if the user with the provided ID is not found.
    """
    user_service = UserService(session)
    return user_service.get_by_id(user_id)


@user_router.post("/", response_model=UserPublic, summary="Create a user",
                  response_description="The created user.", status_code=status.HTTP_201_CREATED)
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
