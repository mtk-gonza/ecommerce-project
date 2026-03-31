# domain/ports/payment_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.payment import Payment
from app.domain.enums import PaymentStatus

class PaymentRepositoryPort(ABC):
    """Puerto de repositorio de pagos"""
    
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        """Crea o actualiza un pago"""
        pass

    @abstractmethod
    def find_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca un pago por ID"""
        pass

    @abstractmethod
    def find_by_order_id(self, order_id: int) -> Optional[Payment]:
        """Busca el pago de una orden"""
        pass

    @abstractmethod
    def find_by_external_id(self, external_id: str) -> Optional[Payment]:
        """Busca un pago por ID externo (MercadoPago)"""
        pass

    @abstractmethod
    def find_by_mp_payment_id(self, mp_payment_id: str) -> Optional[Payment]:
        """Busca un pago por ID de MercadoPago"""
        pass

    @abstractmethod
    def find_by_status(self, status: PaymentStatus, limit: int = 100) -> List[Payment]:
        """Busca pagos por estado"""
        pass

    @abstractmethod
    def find_pending_payments(self, limit: int = 100) -> List[Payment]:
        """Busca pagos pendientes de confirmación"""
        pass

    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        """Elimina un pago (solo si está en estado permitido)"""
        pass