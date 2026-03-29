from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User

class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass