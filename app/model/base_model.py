"""
This module defines a base class with common fields for the SQLAlchemy models.
"""

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql.expression import text
from app.database.database import Base


class BaseModel(Base):
    """
    A base class that includes common fields for most models.

    Attributes:
        created_at (DateTime): The timestamp when the record was created; defaults to current time.
        updated_at (DateTime): The timestamp when the record was last updated.
        deleted_at (DateTime): The timestamp when the record was deleted.
        is_deleted (Boolean): A flag indicating whether the record is deleted, defaults to False.
    """

    __abstract__ = True

    created_at = Column(DateTime(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, server_default='FALSE', nullable=False)
