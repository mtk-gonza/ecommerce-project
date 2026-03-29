from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.domain.enums import UserRole, AddressType

# ==================== ADDRESS SCHEMAS ====================

class AddressBase(BaseModel):
    street: str = Field(..., min_length=5, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: str = Field(..., min_length=5, max_length=20)
    country: str = Field(..., min_length=2, max_length=100)
    type: str = Field(default='both', description='billing, shipping, or both')
    alias: Optional[str] = Field(None, max_length=50)
    is_default: bool = False

class AddressCreateSchema(AddressBase):
    pass

class AddressUpdateSchema(BaseModel):
    street: Optional[str] = Field(None, min_length=5, max_length=255)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, min_length=5, max_length=20)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    type: Optional[str] = Field(None, description='billing, shipping, or both')
    alias: Optional[str] = Field(None, max_length=50)
    is_default: Optional[bool] = None

class AddressSchema(AddressBase):
    id: int
    user_id: int
    address_type: AddressType
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.CUSTOMER

class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=100, description="Password must be at least 8 characters")

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

class UserPasswordUpdateSchema(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=100)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(UserBase):
    id: int
    role: UserRole
    is_active: bool = True  # ← Valor por defecto
    email_verified_at: Optional[datetime] = None
    addresses: List[AddressSchema] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

# ==================== TOKEN SCHEMAS ====================

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSchema

class TokenDataSchema(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

class UserInTokenSchema(BaseModel):
    """Schema ligero para incluir en la respuesta de login/token"""
    id: int
    email: EmailStr
    name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInTokenSchema  # ← Cambiar de UserSchema a UserInTokenSchema

    model_config = ConfigDict(from_attributes=True)

# ==================== RESPONSE SCHEMAS ====================

class UserResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[UserSchema] = None

class UsersListResponseSchema(BaseModel):
    success: bool
    message: str
    data: List[UserSchema]
    total: int
    skip: int
    limit: int

class AddressResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[AddressSchema] = None