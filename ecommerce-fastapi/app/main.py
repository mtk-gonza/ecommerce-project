from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config.settings import settings
from app.interfaces.api.v1.routes import auth_router, user_router, product_router, order_router, cart_router, payment_router
from app.infrastructure.db.session import init_db
from app.infrastructure.logging import setup_logging
from app.infrastructure.exceptions.http_exception_handler import (
    authentication_exception_handler,
    authorization_exception_handler,
    validation_exception_handler,
)
from app.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ValidationError,
)

setup_logging(
    env=settings.ENVIRONMENT,
    log_level=settings.LOG_LEVEL,
    debug=settings.DEBUG,
    log_dir=settings.BASE_DIR / "logs",
    enable_file_logging=True,
    enable_webhook_logging=True,
)

app = FastAPI(title="e-commerce fastapi", version="1.0.0")

# Registrar handlers para excepciones de dominio
app.add_exception_handler(AuthenticationException, authentication_exception_handler)
app.add_exception_handler(AuthorizationException, authorization_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
init_db()

# Include routers
app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(user_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(product_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(order_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(cart_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(payment_router.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "e-commerce fastapi", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}