"""
This module imports the Base class and all models used in the application.

It ensures that Alembic can detect all models for generating migrations.
"""

from app.database.database import Base
from .user import User
