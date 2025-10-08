from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "HTTPException"},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "type": "UnhandledException"},
    )


def register_error_handlers(app):
    """Attach global exception handlers to FastAPI app."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
