from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from app.domain.enums import OrderStatus, Currency
from app.domain.exceptions import ValidationError, BusinessRuleException, OrderAlreadyShippedException

@dataclass
class OrderItem:
    id: Optional[int]
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        if self.unit_price < 0:
            raise ValidationError("El precio unitario no puede ser negativo")

@dataclass
class OrderStatusHistory:
    id: Optional[int]
    order_id: int
    status: OrderStatus
    commented_by: Optional[int] = None
    comment: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Order:
    id: Optional[int]
    order_number: str
    user_id: int
    status: OrderStatus = OrderStatus.PENDING
    currency: Currency = Currency.USD
    shipping_address: str = ""
    billing_address: str = ""
    subtotal: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    shipping_cost: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    items: List[OrderItem] = field(default_factory=list)
    status_history: List[OrderStatusHistory] = field(default_factory=list)
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.order_number:
            raise ValidationError("El número de orden es obligatorio")
        if not self.user_id:
            raise ValidationError("El user_id es obligatorio")
        self._calculate_total()

    def _calculate_total(self):
        self.subtotal = sum(item.total_price for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount

    def add_status_history(self, status: OrderStatus, commented_by: Optional[int] = None, comment: Optional[str] = None):
        history = OrderStatusHistory(id=None, order_id=self.id, status=status, commented_by=commented_by, comment=comment)
        self.status_history.append(history)
        self.status = status
        self.updated_at = datetime.now()

    def confirm(self):
        if self.status != OrderStatus.PENDING:
            raise BusinessRuleException("Solo se pueden confirmar órdenes pendientes")
        self.add_status_history(OrderStatus.CONFIRMED, comment="Orden confirmada")

    def cancel(self, reason: Optional[str] = None):
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise OrderAlreadyShippedException("No se puede cancelar una orden ya enviada")
        self.add_status_history(OrderStatus.CANCELLED, comment=f"Cancelada: {reason}")

    def ship(self, tracking_number: Optional[str] = None):
        if self.status not in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]:
            raise BusinessRuleException("Solo se pueden enviar órdenes confirmadas o en proceso")
        self.add_status_history(OrderStatus.SHIPPED, comment=f"Enviada. Tracking: {tracking_number}")