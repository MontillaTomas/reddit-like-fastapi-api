"""
This module contains the BaseSchema class which defines common fields
for most schemas.
"""

from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Base schema defining common fields for most schemas.

    Attributes:
        created_at (datetime): Timestamp indicating creation time.
        updated_at (datetime, optional): Timestamp indicating last update time.
    """

    created_at: datetime
    updated_at: datetime | None = None
