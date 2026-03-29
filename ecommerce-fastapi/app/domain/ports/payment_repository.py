from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.cart import Cart

class PaymentRepositoryPort(ABC):
    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def find_by_id(self, cart_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Optional[Cart]:
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        pass