from fastapi import APIRouter, Depends, status
from app.interfaces.api.v1.schemas.user_schema import UserCreateSchema, UserLoginSchema, TokenSchema, UserSchema
from app.application.services.auth_service import AuthService
from app.interfaces.api.v1.dependencies.services import get_auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register(
        email=user_data.email, 
        password=user_data.password, 
        name=user_data.name, 
        phone=user_data.phone
    )

@router.post("/login", response_model=TokenSchema)
def login(credentials: UserLoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(
        email=credentials.email,
        password=credentials.password
    )