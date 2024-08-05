"""
This module contains the ProfilePictureService class, which provides methods
for managing profile picture uploads, validations, and storage.
"""

from pathlib import Path
from uuid import uuid4

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

        pfp = ProfilePictureCreate(
            id=uuid4_filename, user_id=user_id, path=str(file_path))

        return self.crud.create(pfp)
