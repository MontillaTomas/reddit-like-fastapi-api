"""
Module for handling profile picture-related API routes and operations in version 1 of the API.

This module defines the pfp_router APIRouter instance for managing profile picture endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, status, Depends, UploadFile
from app.auth.jwt import get_current_user
from app.dependency.pfp_service_dependency import get_pfp_service
from app.schema.pfp import ProfilePicturePublic
from app.schema.user import UserPayload
from app.service.pfp_service import ProfilePictureService

pfp_router = APIRouter(prefix="/me/profile-pictures")


@pfp_router.post("/",
                 response_model=ProfilePicturePublic,
                 summary="Upload a profile picture",
                 response_description="The uploaded profile picture details.",
                 status_code=status.HTTP_201_CREATED)
async def upload_pfp(file: UploadFile,
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


@pfp_router.delete("/",
                   response_model=None,
                   summary="Delete current profile picture",
                   response_description="No content",
                   status_code=status.HTTP_204_NO_CONTENT)
def delete_current_pfp(user_payload: Annotated[UserPayload, Depends(get_current_user)],
                       pfp_service: Annotated[ProfilePictureService, Depends(get_pfp_service)]):
    """
    Delete the current profile picture of the authenticated user.

    Returns no content.

    Raises HTTPException if the user does not have a profile picture.
    """
    return pfp_service.delete_current_profile_picture(user_payload.id)
