from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.order import Order
from app.domain.enums import OrderStatus

class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def find_by_order_number(self, order_number: str) -> Optional[Order]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        pass

    @abstractmethod
    def find_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> bool:
        pass