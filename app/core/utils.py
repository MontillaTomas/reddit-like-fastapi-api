"""
This module provides utility functions for handling common operations
within the application.

Functions:
    convert_datetimes(obj): Recursively converts all datetime objects
    in the input to ISO 8601 strings.
"""
from datetime import datetime


def convert_datetimes(obj):
    """
    Recursively converts all datetime objects in the input to ISO 8601 strings.

    Args:
        obj: The input object which may contain datetime objects.

    Returns:
        The input object with all datetime objects converted to ISO 8601 strings.
    """
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_datetimes(i) for i in obj]
    if isinstance(obj, datetime):
        return obj.isoformat()

    return obj
