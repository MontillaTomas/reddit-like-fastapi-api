"""
This module provides utility functions for creating and verifying JWT tokens
using the PyJWT library.
"""
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer

from app.schema.token import TokenData, Token
from app.schema.user import UserPublic
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# openssl rand -hex 32
SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: TokenData) -> Token:
    """
    Creates a JWT access token with the given data and expiration time.

    Args:
        data (TokenData): The data to encode in the JWT token.

    Returns:
        Token: A Token instance containing the access token, its type, expiration time, and user 
        data.
    """
    to_encode = data.model_dump()

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(
        {**to_encode, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    return Token(access_token=encoded_jwt, expire_time=expire, user=data.user)


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """
    Verifies the validity of a JWT access token.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (Exception): The exception to raise if verification fails.

    Returns:
        TokenData: The decoded token data if verification is successful.

    Raises:
        Exception: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_dict = payload.get("user")

        if user_dict is None:
            raise credentials_exception

        user = UserPublic(**user_dict)
        token_data = TokenData(user=user)
    except jwt.PyJWTError as e:
        raise credentials_exception from e

    return token_data
