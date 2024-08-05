"""
Module defining CRUD operations for profile pictures.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.model.pfp import ProfilePicture
from app.schema.pfp import ProfilePictureCreate


class CRUDPfp:
    """
    This class encapsulates methods to perform CRUD operations on ProfilePicture entities
    in the database.

    Attributes:
        session (Session): SQLAlchemy database session.
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, pfp: ProfilePictureCreate) -> ProfilePicture:
        """
        Creates a new profile picture record in the database.

        Args:
            pfp (ProfilePictureCreate): The schema containing data for the new profile picture.

        Returns:
            ProfilePicture: The newly created profile picture record.
        """
        pfp = ProfilePicture(**pfp.model_dump())
        pfp.uploaded_at = func.now()  # pylint: disable=not-callable
        self.session.add(pfp)
        self.session.commit()
        self.session.refresh(pfp)
        return pfp
