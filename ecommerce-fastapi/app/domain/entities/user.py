from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from app.domain.enums import UserRole, AddressType
from app.domain.exceptions import ValidationError
import re

@dataclass
class Address:
    id: Optional[int]
    street: str
    city: str
    state: Optional[str]
    zip_code: str
    country: str
    address_type: AddressType
    alias: Optional[str] = None
    is_default: bool = False
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.street or not self.city or not self.zip_code or not self.country:
            raise ValidationError("Todos los campos de dirección son obligatorios")

@dataclass
class User:
    id: Optional[int]
    email: str
    password_hash: str
    name: str
    role: UserRole = UserRole.CUSTOMER
    phone: Optional[str] = None
    is_active: bool = True
    email_verified_at: Optional[datetime] = None
    addresses: List[Address] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self._is_valid_email():
            raise ValidationError("Email inválido")
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        if not isinstance(self.role, UserRole):
            raise ValidationError("Rol inválido")

    def _is_valid_email(self) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, self.email))

    def verify_email(self):
        self.email_verified_at = datetime.now()

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN