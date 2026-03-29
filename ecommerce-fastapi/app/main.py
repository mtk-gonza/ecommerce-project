from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.interfaces.api.v1.routes import auth_router, user_router, product_router, order_router, cart_router
from app.infrastructure.db.session import init_db

app = FastAPI(title="e-commerce fastapi", version="1.0.0")

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

@app.get("/")
def root():
    return {"message": "e-commerce fastapi", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}