"""
This module provides utility functions for password hashing and verification
using the Passlib library with bcrypt.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(password, hashed_password)
