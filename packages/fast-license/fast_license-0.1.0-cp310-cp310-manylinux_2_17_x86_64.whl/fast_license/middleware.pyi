import pathlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

class LicenseMiddleware(BaseHTTPMiddleware):
    license_path: pathlib.Path
    private_key: str
    def __init__(self, app: ASGIApp, license_path: pathlib.Path, private_key: str) -> None: ...
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response: ...
