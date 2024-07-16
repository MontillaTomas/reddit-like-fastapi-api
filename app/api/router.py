"""
Router module for defining API routers.

This module creates an APIRouter instance that includes other routers.
"""

from fastapi import APIRouter
from app.api.v1.user import user_router

router = APIRouter()

router.include_router(user_router)
