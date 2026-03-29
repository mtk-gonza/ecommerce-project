from app.domain.entities.user import User, Address
from app.infrastructure.db.models.user_model import UserModel, AddressModel
from typing import List

class UserMapper:
    @staticmethod
    def to_entity(model: UserModel) -> User:
        addresses = [
            Address(
                id=addr.id,
                street=addr.street,
                city=addr.city,
                state=addr.state,
                zip_code=addr.zip_code,
                country=addr.country,
                address_type=addr.address_type,
                alias=addr.alias,
                is_default=addr.is_default,
                created_at=addr.created_at
            )
            for addr in model.addresses
        ]
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            name=model.name,
            role=model.role,
            phone=model.phone,
            is_active=model.is_active,
            email_verified_at=model.email_verified_at,
            addresses=addresses,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            name=entity.name,
            role=entity.role,
            phone=entity.phone,
            is_active=entity.is_active,
            email_verified_at=entity.email_verified_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )