from fastapi import Request
from fastapi.responses import JSONResponse
from ..domain.errors import DomainError

async def domain_error_handler(request: Request, exc: DomainError):  # noqa: ARG001
    return JSONResponse(
        status_code=400,
        content={"error": {"type": "domain_error", "message": str(exc)}},
    )

async def generic_error_handler(request: Request, exc: Exception):  # noqa: ARG001
    return JSONResponse(
        status_code=500,
        content={"error": {"type": "server_error", "message": "Internal server error"}},
    )
