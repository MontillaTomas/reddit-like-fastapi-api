"""
This module defines a base schema class with common fields for models with soft delete 
functionality.
"""
from datetime import datetime
from pydantic import BaseModel


class DeletedSchema(BaseModel):
    """
    Base schema defining fields for models with soft delete functionality.

    Attributes:
        deleted_at (datetime, optional): Timestamp indicating deletion time.
        is_deleted (bool): Flag indicating if the record is deleted.
    """

    deleted_at: datetime | None = None
    is_deleted: bool = False
