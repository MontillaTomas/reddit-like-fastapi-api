"""
Module for defining user-related API routes and operations in version 1 of the API.

This module defines the user_router APIRouter instance for managing user endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, status, Depends
from app.auth.jwt import get_current_user
from app.dependency.user_service_dependency import get_user_service
from app.schema.user import UserCreate, UserPublic, UserUpdateUsername, UserUpdatePassword, UserDelete, UserPayload
from app.service.user_service import UserService
from app.api.v1.pfp import pfp_router

user_router = APIRouter(prefix="/v1/users", tags=["Users"])


@user_router.get("/{user_id}",
                 response_model=UserPublic,
                 summary="Get a user by ID",
                 response_description="The user with the provided ID.",
                 status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    """
    Get a user by its ID.

    - **user_id**: ID of the user to retrieve.

    Returns the user with the provided ID.

    Raises HTTPException if the user with the provided ID is not found.
    """
    return user_service.get_by_id(user_id)


@user_router.post("/",
                  response_model=UserPublic,
                  summary="Create a user",
                  response_description="The created user.",
                  status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: Annotated[UserService, Depends(get_user_service)]):
    """
    Create a new user.

    - **email**: Email address of the user.
    - **username**: Username of the user.
    - **password**: Password of the user.

    Returns the created user.

    Raises HTTPException if the username or email is already registered.
    """
    return user_service.create(user)


@user_router.put("/me/username",
                 response_model=UserPublic,
                 summary="Update a user's username",
                 response_description="The updated user.",
                 status_code=status.HTTP_200_OK)
def update_user_username(user_payload: Annotated[UserPayload, Depends(get_current_user)],
                         new_username: UserUpdateUsername,
                         user_service: Annotated[UserService, Depends(get_user_service)]):
    """
    Update a user's username.

    - **user_payload**: Payload containing the user's information from the JWT token.
    - **new_username**: New username for the user.

    Returns the updated user.

    Raises HTTPException if the user with the provided ID is not found or if the username is 
    already registered or if the new username is the same as the old username.
    """
    return user_service.update_username(user_payload.id, new_username)


@user_router.put("/me/password",
                 response_model=UserPublic,
                 summary="Update a user's password",
                 response_description="The updated user.",
                 status_code=status.HTTP_200_OK)
def update_user_password(user_payload: Annotated[UserPayload, Depends(get_current_user)],
                         user_passwords: UserUpdatePassword,
                         user_service: Annotated[UserService, Depends(get_user_service)]):
    """
    Update a user's password.

    - **user_payload**: Payload containing the user's information from the JWT token.
    - **user_passwords**: New and old passwords for the user.

    Returns the updated user.

    Raises HTTPException if the user with the provided ID is not found or if the old password is
    incorrect or if the new password is the same as the old password.
    """
    return user_service.update_password(user_payload.id, user_passwords)


@user_router.delete("/me",
                    response_model=None,
                    summary="Delete a user",
                    response_description="No content",
                    status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_payload: Annotated[UserPayload, Depends(get_current_user)],
                password: UserDelete,
                user_service: Annotated[UserService, Depends(get_user_service)]):
    """
    Delete a user.

    - **user_payload**: Payload containing the user's information from the JWT token.
    - **password**: Password of the user.

    Returns no content.

    Raises HTTPException if the user with the provided ID is not found or if the password is 
    incorrect.
    """
    return user_service.delete(user_payload.id, password)


user_router.include_router(pfp_router)
