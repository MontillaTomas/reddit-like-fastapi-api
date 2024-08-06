"""
This module defines the SQLAlchemy model for the User table.
"""

from sqlalchemy import Column, BigInteger, String, Index
from .base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the application.

    Attributes:
        id (BigInteger): The primary key of the user.
        email (String): The email of the user, must be unique.
        username (String): The username of the user, must be unique.
        password (String): The hashed password of the user.
        created_at (DateTime): The timestamp when the record was created; defaults to current time.
        updated_at (DateTime): The timestamp when the record was last updated.
    """

    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(60), nullable=False)


Index('user_email_index', User.email)
Index('user_username_index', User.username)
