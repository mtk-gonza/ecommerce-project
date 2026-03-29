from typing import List, Optional
from app.domain.entities.user import User, Address
from app.domain.enums import UserRole, AddressType
from app.domain.ports.user_repository import UserRepositoryPort
from app.domain.exceptions import EntityNotFoundException, ValidationError
from app.infrastructure.security.password_handler import hash_password, verify_password

class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def create_user(self, email: str, password: str, name: str, role: UserRole = UserRole.CUSTOMER, phone: Optional[str] = None) -> User:
        # Verificar email único
        existing = self.user_repository.find_by_email(email)
        if existing:
            raise ValidationError(f"El email {email} ya está registrado")
        
        # Hashear password
        password_hash = hash_password(password)
        
        user = User(
            id=None,
            email=email,
            password_hash=password_hash,
            name=name,
            role=role,
            phone=phone,
            is_active=True
        )
        return self.user_repository.save(user)

    def get_user(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"Usuario {user_id} no encontrado")
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.find_by_email(email)

    def update_user(self, user_id: int, user_data: dict) -> User:
        user = self.get_user(user_id)
        for key, value in user_data.items():
            if hasattr(user, key) and key not in ['id', 'password_hash', 'created_at']:
                setattr(user, key, value)
        user._validate()
        return self.user_repository.save(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        return self.user_repository.delete(user_id)

    def verify_password(self, user: User, password: str) -> bool:
        return verify_password(password, user.password_hash)

    def add_address(self, user_id: int, address_data: dict) -> User:
        user = self.get_user(user_id)
        address = Address(
            id=None,
            street=address_data['street'],
            city=address_data['city'],
            state=address_data.get('state'),
            zip_code=address_data['zip_code'],
            country=address_data['country'],
            address_type=AddressType(address_data.get('type', 'both')),
            alias=address_data.get('alias'),
            is_default=address_data.get('is_default', False)
        )
        user.add_address(address)
        return self.user_repository.save(user)

    def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        user = self.get_user(user_id)
        if not self.verify_password(user, old_password):
            raise ValidationError("Contraseña actual incorrecta")
        user.password_hash = hash_password(new_password)
        return self.user_repository.save(user)