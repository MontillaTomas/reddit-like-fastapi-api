"""
Module defining CRUD operations for profile pictures.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_
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

    def delete_current_pfp(self, user_id: int) -> ProfilePicture:
        """
        Soft deletes the current profile picture of a user.

        Args:
            user_id (int): The ID of the user whose profile picture is to be deleted.

        Returns:
            ProfilePicture: The profile picture record that was soft deleted.
        """
        last_pfp = self.session.query(ProfilePicture).filter(
            and_(ProfilePicture.user_id == user_id,
                 ProfilePicture.is_deleted.is_(False))
        ).first()

        if last_pfp:
            last_pfp.deleted_at = func.now()  # pylint: disable=not-callable
            last_pfp.is_deleted = True

        self.session.commit()
        return last_pfp

    def get_by_id(self, pfp_uuid: UUID) -> ProfilePicture:
        """
        Retrieves a profile picture record by its UUID.

        Args:
            pfp_uuid (UUID): The UUID of the profile picture to retrieve.

        Returns:
            ProfilePicture: The profile picture record with the provided UUID.
        """
        return self.session.query(ProfilePicture).filter(ProfilePicture.id == pfp_uuid).first()

    def get_by_user_id(self, user_id: int) -> ProfilePicture:
        """
        Retrieves the current profile picture of a user.

        Args:
            user_id (int): The ID of the user whose profile picture is to be retrieved.

        Returns:
            ProfilePicture: The profile picture record of the user.
        """
        return self.session.query(ProfilePicture).filter(
            and_(ProfilePicture.user_id == user_id,
                 ProfilePicture.is_deleted.is_(False))
        ).first()
