"""
Module for handling authentication routes using FastAPI.

This module defines the API endpoints related to user authentication,
including login functionality.
"""

from typing import Annotated
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.token import Token
from app.service.auth_service import AuthService

auth_router = APIRouter(prefix="/v1", tags=["Authentication"])


@auth_router.post("/login",
                  response_model=Token,
                  summary="Authenticate a user",
                  response_description="The access token for the user.",
                  status_code=status.HTTP_200_OK)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
          session: Annotated[Session, Depends(get_db)]):
    """
    Authenticate a user by providing the username (or email) and password.

    - **username**: The username (or email) of the user.
    - **password**: The password of the user.

    Returns the access token for the user.

    Raises HTTPException if the user is not found or the password is incorrect.
    """
    auth_service = AuthService(session)
    return auth_service.authenticate_user(user_credentials.username, user_credentials.password)
