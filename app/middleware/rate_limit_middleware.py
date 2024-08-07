"""
This module defines a middleware class that enforces rate limiting on HTTP requests
based on the client's IP address and request path.
"""

import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware class that enforces rate limiting on HTTP requests.

    This middleware restricts the number of requests that a client can make
    in a given time period based on the client's IP address and request path.
    """

    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[Tuple[str,
                                            str], float] = defaultdict(float)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Processes an incoming request and applies rate limiting.

        Args:
            request (Request): The incoming HTTP request.
            call_next (function): The next callable in the request/response cycle.

        Returns:
            Response: The HTTP response, either allowing the request to proceed or
                      returning a 429 Too Many Requests status if the rate limit is exceeded.

        The rate limit is set to 1 request per second for each client IP and request path.
        """
        client_ip = request.client.host
        path = request.url.path
        current_time = time.time()

        key = (client_ip, path)

        # 1 request per second limit
        if current_time - self.rate_limit_records[key] < 1:
            return Response(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json",
                content="{\"detail\": \"Rate limit exceeded. Try again in a second.\"}"
            )

        self.rate_limit_records[key] = current_time

        response = await call_next(request)

        return response
