"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI
from app.api.router import router
from app.middleware.process_time_header_middleware import ProcessTimeHeaderMiddleware

app = FastAPI()

app.add_middleware(ProcessTimeHeaderMiddleware)

app.include_router(router)
