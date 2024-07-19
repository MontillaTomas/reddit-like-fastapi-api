"""
This module defines the SQLAlchemy model for the User table.
"""

from sqlalchemy import Column, BigInteger, String
from .base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the application.

    Attributes:
        id (BigInteger): The primary key of the user.
        email (String): The email of the user, must be unique.
        username (String): The username of the user, must be unique.
        password (String): The hashed password of the user.
    """

    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
