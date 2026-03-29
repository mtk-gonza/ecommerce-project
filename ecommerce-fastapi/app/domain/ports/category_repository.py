from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.category import Category

class CategoryRepositoryPort(ABC):
    @abstractmethod
    def save(self, cart: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, cart_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Optional[Category]:
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        pass