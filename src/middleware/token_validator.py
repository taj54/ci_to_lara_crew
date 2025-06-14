from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, expected_token: str):
        super().__init__(app)
        self.expected_token = expected_token

    async def dispatch(self, request: Request, call_next):
        x_token = request.headers.get("x-token")
        if x_token != self.expected_token:
            raise HTTPException(status_code=400, detail="X-Token header invalid")
        return await call_next(request)
