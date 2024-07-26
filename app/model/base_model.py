"""
This module defines a base class with common fields for the SQLAlchemy models.
"""

from sqlalchemy import Column, DateTime
from sqlalchemy.sql.expression import text
from app.database.database import Base


class BaseModel(Base):
    """
    A base class that includes common fields for most models.

    Attributes:
        created_at (DateTime): The timestamp when the record was created; defaults to current time.
        updated_at (DateTime): The timestamp when the record was last updated.
    """

    __abstract__ = True

    created_at = Column(DateTime(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
