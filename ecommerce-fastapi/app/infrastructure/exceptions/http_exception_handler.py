from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.domain.exceptions import AuthenticationException, AuthorizationException, ValidationError
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)

async def authentication_exception_handler(request: Request, exc: AuthenticationException):
    """Convierte AuthenticationException en HTTP 401"""
    logger.warning(f"🔍 AUTH_HANDLER ACTIVADO: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )

async def authorization_exception_handler(request: Request, exc: AuthorizationException):
    logger.warning(f"🔍 AUTHZ_HANDLER ACTIVADO: {exc}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"🔍 VALIDATION_HANDLER ACTIVADO: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )