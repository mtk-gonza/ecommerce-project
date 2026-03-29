from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepositoryPort
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.mappers.user_mapper import UserMapper

class UserRepositoryImpl(UserRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        model = UserMapper.to_model(user)
        if user.id:
            self.db.merge(model)
        else:
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return UserMapper.to_entity(model)

    def find_by_id(self, user_id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return UserMapper.to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return UserMapper.to_entity(model) if model else None

    def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        models = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [UserMapper.to_entity(m) for m in models]

    def delete(self, user_id: int) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True