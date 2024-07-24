"""
Module for handling user authentication and token creation.

This module provides the AuthService class which includes methods for authenticating a user
by verifying their credentials and generating JWT tokens.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.crud_user import CRUDUser
from app.auth.jwt import create_access_token
from app.core.pw_utils import verify_password
from app.schema.token import TokenData, Token
from app.schema.user import UserPayload


class AuthService:
    """
    Service for handling authentication-related operations.

    This class provides methods to authenticate users and generate access tokens.

    Attributes:
        crud (CRUDUser): Instance of CRUD operations for User entities.
    """

    def __init__(self, session: Session):
        self.crud = CRUDUser(session)

    def authenticate_user(self, identifier: str, password: str) -> Token:
        """
        Authenticates a user by verifying the identifier (username or email) and password.

        Args:
            identifier (str): The username or email of the user.
            password (str): The password of the user.

        Returns:
            Token: A Token instance containing the access token and user data.

        Raises:
            HTTPException: If the user is not found or the password is incorrect.
        """
        user = self.crud.get_by_username(identifier)

        if user is None:
            user = self.crud.get_by_email(identifier)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

        user = UserPayload(**user.__dict__)

        token_data = TokenData(user=user)

        return create_access_token(token_data)
