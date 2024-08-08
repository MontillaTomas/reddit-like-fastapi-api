"""
This module contains the ProfilePictureService class, which provides methods
for managing profile picture uploads, validations, and storage.
"""

from pathlib import Path
from uuid import uuid4, UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.crud.crud_pfp import CRUDPfp
from app.schema.pfp import ProfilePictureCreate, ProfilePicturePublic

IMAGE_FORMATS = {"image/jpeg", "image/png", "image/gif"}
MEGABYTE = 1024 * 1024
MAX_FILE_SIZE = 2 * MEGABYTE
UPLOAD_DIR = Path("./media/pfp")
# Ensure the upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ProfilePictureService:
    """
    Service for managing profile pictures.

    Attributes:
        crud (CRUDPfp): The CRUD utility for interacting with the profile picture table.
    """

    def __init__(self, session: Session):
        self.crud = CRUDPfp(session)

    async def save_profile_picture(self, user_id: int, file: UploadFile) -> ProfilePicturePublic:
        """
        Creates a new profile picture record after validating and storing the file.

        Args:
            user_id (int): The ID of the user uploading the profile picture.
            file (UploadFile): The file object containing the profile picture.

        Returns:
            ProfilePicturePublic: The public schema of the created profile picture.

        Raises:
            HTTPException: If the file format is unsupported, file size exceeds the limit,
                           or an error occurs while saving the file.
        """
        if file.content_type not in IMAGE_FORMATS:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="Unsupported media type. Only JPEG, PNG, and GIF images are supported.")

        if file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                detail="File is too large. The maximum file size allowed is 2MB.")

        uuid4_filename = uuid4()
        file_extension = file.filename.split(".")[-1]
        filename = f"{uuid4_filename}.{file_extension}"
        file_path = UPLOAD_DIR / filename

        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while saving the file: {str(e)}") from e

        prev_pfp = self.crud.delete_current_pfp(user_id)

        # remove the previous profile picture file
        if prev_pfp:
            prev_file_path = Path(prev_pfp.path)
            prev_file_path.unlink(missing_ok=True)

        pfp = ProfilePictureCreate(
            id=uuid4_filename, user_id=user_id, path=str(file_path))

        return self.crud.create(pfp)

    def delete_current_profile_picture(self, user_id: int) -> None:
        """
        Deletes the current profile picture of a user.

        Args:
            user_id (int): The ID of the user whose profile picture is to be deleted.

        Raises:
            HTTPException: If the user does not have a profile picture.

        Returns:
            None
        """
        pfp = self.crud.get_by_user_id(user_id)

        if not pfp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not have a profile picture.")

        file_path = Path(pfp.path)
        file_path.unlink(missing_ok=True)

        self.crud.delete_current_pfp(user_id)

        return None

    def get_by_id(self, pfp_uuid: UUID) -> ProfilePicturePublic:
        """
        Retrieves a profile picture record by its UUID.

        Args:
            pfp_uuid (UUID): The UUID of the profile picture to retrieve.

        Returns:
            ProfilePicturePublic: The public schema of the profile picture record with the provided
            UUID.
        """
        pfp = self.crud.get_by_id(pfp_uuid)
        if not pfp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Profile picture not found.")
        return pfp
