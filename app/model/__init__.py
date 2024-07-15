"""
Initialize the Base class and metadata for SQLAlchemy models.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
