"""
This module defines a deleted model class with common fields for models with soft delete 
functionality.
"""
from sqlalchemy import Column, DateTime, Boolean
from app.database.database import Base


class DeletedModel(Base):
    """
    A base class that includes common fields for models with soft delete functionality.


    Atrributes:
        deleted_at (DateTime): The timestamp when the record was deleted.
        is_deleted (Boolean): A flag indicating whether the record is deleted, defaults to False.
    """
    __abstract__ = True

    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, server_default='FALSE', nullable=False)
