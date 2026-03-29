from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.coupon import Coupon

class CouponRepositoryPort(ABC):
    @abstractmethod
    def save(self, cart: Coupon) -> Coupon:
        pass

    @abstractmethod
    def find_by_id(self, cart_id: int) -> Optional[Coupon]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Coupon]:
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Optional[Coupon]:
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        pass