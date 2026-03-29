from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.domain.enums import PaymentStatus
from app.domain.exceptions import ValidationError, BusinessRuleException

@dataclass
class Payment:
    id: Optional[int]
    order_id: int
    amount: Decimal
    payment_method: str  # 'card', 'paypal', 'transfer', etc.
    transaction_id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    paid_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.order_id:
            raise ValidationError("El order_id es obligatorio")
        if self.amount <= 0:
            raise ValidationError("El monto debe ser mayor a 0")
        if not isinstance(self.status, PaymentStatus):
            raise ValidationError("Estado de pago inválido")

    def complete(self, transaction_id: str):
        """Completa el pago"""
        if self.status != PaymentStatus.PENDING:
            raise BusinessRuleException("Solo se pueden completar pagos pendientes")
        self.status = PaymentStatus.COMPLETED
        self.transaction_id = transaction_id
        self.paid_at = datetime.now()
        self.updated_at = datetime.now()

    def fail(self, reason: Optional[str] = None):
        """Marca el pago como fallido"""
        if self.status != PaymentStatus.PENDING:
            raise BusinessRuleException("Solo se pueden fallar pagos pendientes")
        self.status = PaymentStatus.FAILED
        self.updated_at = datetime.now()

    def refund(self, amount: Optional[Decimal] = None):
        """Reembolsa el pago"""
        if self.status != PaymentStatus.COMPLETED:
            raise BusinessRuleException("Solo se pueden reembolsar pagos completados")
        
        if amount is None or amount == self.amount:
            self.status = PaymentStatus.REFUNDED
        else:
            self.status = PaymentStatus.PARTIALLY_REFUNDED
        
        self.updated_at = datetime.now()

    @property
    def is_completed(self) -> bool:
        return self.status == PaymentStatus.COMPLETED

    @property
    def is_pending(self) -> bool:
        return self.status == PaymentStatus.PENDING