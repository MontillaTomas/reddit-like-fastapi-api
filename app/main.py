"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI
from app.api.router import router
from app.middleware.process_time_header_middleware import ProcessTimeHeaderMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware

app = FastAPI()

app.add_middleware(ProcessTimeHeaderMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(router)
