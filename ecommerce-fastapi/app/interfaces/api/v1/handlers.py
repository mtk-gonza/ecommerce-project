from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    ApplicationError,
    NotFoundError,
    ValidationError,
    ConflictError
)

from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

# =========================
# 🔹 MAPEO EXCEPCIONES → HTTP
# =========================
EXCEPTION_STATUS_MAP = {
    NotFoundError: 404,
    ValidationError: 400,
    ConflictError: 409,
}


def get_status_code(exc: ApplicationError) -> int:
    """
    Soporta herencia de excepciones (MUY importante)
    """
    for exc_type, status in EXCEPTION_STATUS_MAP.items():
        if isinstance(exc, exc_type):
            return status
    return 500


# =========================
# 🔹 REGISTRO HANDLERS
# =========================
def register_exception_handlers(app):

    # 🔹 Errores de dominio (los tuyos)
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError):
        status_code = get_status_code(exc)

        message = getattr(exc, "message", str(exc))
        code = getattr(exc, "code", "error")

        # Logging
        if status_code >= 500:
            logger.exception(f"[{request.method}] {request.url} - {message}")
        else:
            logger.warning(f"[{request.method}] {request.url} - {message}")

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": message
                }
            }
        )

    # 🔹 Fallback global (errores inesperados)
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception(f"[{request.method}] {request.url} - Unexpected error")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error"
                }
            }
        )