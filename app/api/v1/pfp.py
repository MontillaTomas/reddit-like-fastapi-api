"""
Module for handling profile picture-related API routes and operations in version 1 of the API.

This module defines the pfp_router APIRouter instance for managing profile picture endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, status, Depends, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.jwt import get_current_user
from app.schema.pfp import ProfilePicturePublic
from app.schema.user import UserPayload
from app.service.pfp_service import ProfilePictureService

pfp_router = APIRouter(prefix="/profile-pictures")


@pfp_router.post("/",
                 response_model=ProfilePicturePublic,
                 summary="Upload a profile picture",
                 response_description="The uploaded profile picture details.",
                 status_code=status.HTTP_201_CREATED)
async def upload_profile_picture(file: UploadFile,
                                 user_payload: Annotated[UserPayload, Depends(get_current_user)],
                                 session: Annotated[Session, Depends(get_db)]):
    """
    Upload a profile picture for the authenticated user.

    - **file**: The image file to upload.

    Returns the uploaded profile picture details.

    Raises HTTPException if the file format is unsupported or the file size exceeds the limit
    or an error occurs while saving the file.
    """
    pfp_service = ProfilePictureService(session)
    return await pfp_service.save_profile_picture(user_payload.id, file)
