"""
Module for handling profile picture-related API routes and operations in version 1 of the API.

This module defines the pfp_router APIRouter instance for managing profile picture endpoints.
"""

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends, UploadFile
from app.auth.jwt import get_current_user
from app.dependency.pfp_service_dependency import get_pfp_service
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
                                 pfp_service: Annotated[ProfilePictureService, Depends(get_pfp_service)]):
    """
    Upload a profile picture for the authenticated user.

    - **file**: The image file to upload.

    Returns the uploaded profile picture details.

    Raises HTTPException if the file format is unsupported or the file size exceeds the limit
    or an error occurs while saving the file.
    """
    return await pfp_service.save_profile_picture(user_payload.id, file)


@pfp_router.get("/{pfp_id}",
                response_model=ProfilePicturePublic,
                summary="Get a profile picture by ID",
                response_description="The profile picture with the provided ID.",
                status_code=status.HTTP_200_OK)
def get_profile_picture_by_id(pfp_id: UUID,
                              pfp_service: Annotated[ProfilePictureService, Depends(get_pfp_service)]):
    """
    Get a profile picture by its ID.

    - **pfp_id**: ID of the profile picture to retrieve.

    Returns the profile picture with the provided ID.

    Raises HTTPException if the profile picture with the provided ID is not found.
    """
    return pfp_service.get_by_id(pfp_id)
