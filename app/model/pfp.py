"""
This module defines the SQLAlchemy model for the User table.
"""
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger
from .deleted_model import DeletedModel


class ProfilePicture(DeletedModel):
    """
    Represents a user's profile picture in the database.

    Attributes:
        id (UUID): The primary key of the profile picture.
        user_id (BigInteger): The foreign key of the user.
        path (String): The path to the profile picture.
        uploaded_at (DateTime): The date and time the profile picture was uploaded.
        deleted_at (DateTime): The timestamp when the record was deleted.
        is_deleted (Boolean): A flag indicating whether the record is deleted, defaults to False.
    """
    __tablename__ = 'profile_picture'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    path = Column(String(255), nullable=False, unique=True)
    uploaded_at = Column(DateTime(timezone=True), nullable=True)
