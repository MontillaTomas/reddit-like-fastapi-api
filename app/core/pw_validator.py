"""
This module provides functions for validating passwords.
"""

import re


def validate_password(value: str) -> str:
    """
    Validate the password.

    Args:
        value (str): The password to be validated.

    Raises:
        ValueError: If the password does not meet the required criteria.

    Returns:
        str: The validated password.
    """
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[@#$%^&+=-]", value):
        raise ValueError(
            "Password must contain at least one special character from [@#$%^&+=-]")
    return value
