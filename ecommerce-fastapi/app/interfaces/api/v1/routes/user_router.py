from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.interfaces.api.v1.schemas.user_schema import UserSchema, UserUpdateSchema, AddressCreateSchema, AddressSchema
from app.application.services.user_service import UserService
from app.interfaces.api.v1.dependencies.services import get_user_service
from app.interfaces.api.v1.dependencies.auth import get_current_user, get_current_admin_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, ValidationError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(user_data: UserUpdateSchema, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        return user_service.update_user(current_user.id, user_data.model_dump(exclude_unset=True))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/me/addresses", response_model=UserSchema)
def add_address(address_data: AddressCreateSchema, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        return user_service.add_address(current_user.id, address_data.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[UserSchema])
def list_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_admin_user)):
    return user_service.user_repository.find_all(skip=skip, limit=limit)