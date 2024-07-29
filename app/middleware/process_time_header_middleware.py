"""
Middleware module for adding process time header to HTTP responses.
"""

import time

from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware class that adds a 'X-Process-Time' header to HTTP responses.

    This middleware measures the time taken to process each request and includes
    this information in the response headers.
    """

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Add 'X-Process-Time' header to the response.

        Args:
            request (Request): The incoming HTTP request.
            call_next (function): The next callable in the request/response cycle.

        Returns:
            Response: The HTTP response with the added 'X-Process-Time' header.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
