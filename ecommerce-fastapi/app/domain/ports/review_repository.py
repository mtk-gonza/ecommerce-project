from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.review import Review

class ReviewRepositoryPort(ABC):
    @abstractmethod
    def save(self, cart: Review) -> Review:
        pass

    @abstractmethod
    def find_by_id(self, cart_id: int) -> Optional[Review]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Review]:
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Optional[Review]:
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        pass