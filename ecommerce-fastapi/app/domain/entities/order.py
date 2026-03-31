from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from app.domain.enums import OrderStatus, Currency, PaymentStatus
from app.domain.exceptions import ValidationError, BusinessRuleException, OrderAlreadyShippedException

if TYPE_CHECKING:
    from app.domain.entities.user import User
    from app.domain.entities.product import Product

@dataclass
class OrderItem:
    """Item individual dentro de una orden"""
    id: Optional[int]
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal  # quantity * unit_price (snapshot al momento de compra)

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        if self.unit_price < 0:
            raise ValidationError("El precio unitario no puede ser negativo")
        if self.total_price != self.quantity * self.unit_price:
            # Recalcular para consistencia
            self.total_price = self.quantity * self.unit_price

@dataclass
class OrderStatusHistory:
    """Historial de cambios de estado de una orden"""
    id: Optional[int]
    order_id: int
    status: OrderStatus
    commented_by: Optional[int] = None  # ID del admin que cambió el estado
    comment: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Order:
    """
    Entidad de Orden - Representa una compra completada por un usuario
    """
    # ==================== CAMPOS OBLIGATORIOS ====================
    id: Optional[int]
    order_number: str  # Único, ej: "ORD-2024-001234"
    user_id: int
    
    # ==================== CAMPOS CON DEFAULT ====================
    status: OrderStatus = OrderStatus.PENDING
    currency: Currency = Currency.USD
    
    # Snapshot de direcciones (texto plano para historial inmutable)
    shipping_address: str = ""
    billing_address: str = ""
    
    # Montos (snapshot al momento de la compra)
    subtotal: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    shipping_cost: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    
    # Items de la orden (snapshot de productos al momento de compra)
    items: List[OrderItem] = field(default_factory=list)
    
    # Historial de estados
    status_history: List[OrderStatusHistory] = field(default_factory=list)
    
    # Metadata
    notes: Optional[str] = None
    payment_reference: Optional[str] = None  # ID de transacción de pasarela
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relaciones (opcional, se cargan por separado)
    user: Optional['User'] = None

    def __post_init__(self):
        self._validate()
        if self.total_amount == 0 and self.items:
            self._calculate_totals()

    def _validate(self):
        """Validaciones de negocio"""
        if not self.order_number or len(self.order_number.strip()) == 0:
            raise ValidationError("El número de orden es obligatorio")
        if not self.user_id:
            raise ValidationError("El user_id es obligatorio")
        if not isinstance(self.status, OrderStatus):
            raise ValidationError("Estado de orden inválido")
        if not isinstance(self.currency, Currency):
            raise ValidationError("Moneda inválida")
        if self.subtotal < 0:
            raise ValidationError("El subtotal no puede ser negativo")
        if not self.items:
            raise ValidationError("La orden debe tener al menos un item")

    def _calculate_totals(self):
        """Recalcula todos los totales de la orden"""
        self.subtotal = sum(item.total_price for item in self.items)
        # Tax: 16% IVA (ajustar según país)
        self.tax_amount = self.subtotal * Decimal("0.16")
        # Shipping: gratis si subtotal >= 500
        self.shipping_cost = Decimal("0") if self.subtotal >= Decimal("500") else Decimal("50")
        # Total final
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount

    # ==================== PROPIEDADES ====================
    
    @property
    def total_items(self) -> int:
        """Cantidad total de productos (sumando cantidades)"""
        return sum(item.quantity for item in self.items)

    @property
    def unique_items(self) -> int:
        """Cantidad de productos únicos"""
        return len(self.items)

    @property
    def can_be_cancelled(self) -> bool:
        """¿Se puede cancelar esta orden?"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    @property
    def can_be_modified(self) -> bool:
        """¿Se puede modificar esta orden?"""
        return self.status == OrderStatus.PENDING

    @property
    def is_paid(self) -> bool:
        """¿La orden está pagada?"""
        return self.status in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING, 
                              OrderStatus.SHIPPED, OrderStatus.DELIVERED]

    # ==================== MÉTODOS DE ESTADO ====================
    
    def add_status_history(self, new_status: OrderStatus, commented_by: Optional[int] = None, comment: Optional[str] = None):
        """Agrega un cambio de estado al historial"""
        history = OrderStatusHistory(
            id=None,
            order_id=self.id,
            status=new_status,
            commented_by=commented_by,
            comment=comment
        )
        self.status_history.append(history)
        self.status = new_status
        self.updated_at = datetime.now()

    def confirm(self, commented_by: Optional[int] = None):
        """Confirma la orden (paso previo al procesamiento)"""
        if self.status != OrderStatus.PENDING:
            raise BusinessRuleException(f"Solo se pueden confirmar órdenes pendientes. Estado actual: {self.status.value}")
        self.add_status_history(OrderStatus.CONFIRMED, commented_by, "Orden confirmada por el sistema")

    def start_processing(self, commented_by: Optional[int] = None):
        """Inicia el procesamiento de la orden (preparación para envío)"""
        if self.status != OrderStatus.CONFIRMED:
            raise BusinessRuleException(f"Solo se pueden procesar órdenes confirmadas. Estado actual: {self.status.value}")
        self.add_status_history(OrderStatus.PROCESSING, commented_by, "Orden en preparación para envío")

    def ship(self, tracking_number: Optional[str] = None, commented_by: Optional[int] = None):
        """Marca la orden como enviada"""
        if self.status not in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]:
            raise BusinessRuleException(f"Solo se pueden enviar órdenes confirmadas o en proceso. Estado actual: {self.status.value}")
        comment = f"Orden enviada. Tracking: {tracking_number}" if tracking_number else "Orden enviada"
        self.add_status_history(OrderStatus.SHIPPED, commented_by, comment)

    def deliver(self, commented_by: Optional[int] = None):
        """Marca la orden como entregada"""
        if self.status != OrderStatus.SHIPPED:
            raise BusinessRuleException(f"Solo se pueden entregar órdenes enviadas. Estado actual: {self.status.value}")
        self.add_status_history(OrderStatus.DELIVERED, commented_by, "Orden entregada al cliente")

    def cancel(self, reason: Optional[str] = None, commented_by: Optional[int] = None):
        """
        Cancela la orden.
        IMPORTANTE: El servicio debe restaurar el stock después de llamar a este método.
        """
        if not self.can_be_cancelled:
            raise OrderAlreadyShippedException(f"No se puede cancelar una orden en estado '{self.status.value}'")
        
        comment = f"Cancelada: {reason}" if reason else "Orden cancelada por el cliente"
        self.add_status_history(OrderStatus.CANCELLED, commented_by, comment)

    def refund(self, amount: Optional[Decimal] = None, commented_by: Optional[int] = None):
        """Procesa un reembolso (parcial o total)"""
        if not self.is_paid:
            raise BusinessRuleException("Solo se pueden reembolsar órdenes pagadas")
        
        refund_amount = amount if amount else self.total_amount
        comment = f"Reembolso procesado: ${refund_amount}"
        self.add_status_history(OrderStatus.REFUNDED, commented_by, comment)

    # ==================== MÉTODOS DE CONSULTA ====================
    
    def get_item(self, product_id: int) -> Optional[OrderItem]:
        """Obtiene un item de la orden por product_id"""
        return next((item for item in self.items if item.product_id == product_id), None)

    def contains_product(self, product_id: int) -> bool:
        """Verifica si la orden contiene un producto específico"""
        return self.get_item(product_id) is not None

    def get_product_quantity(self, product_id: int) -> int:
        """Obtiene la cantidad de un producto en la orden"""
        item = self.get_item(product_id)
        return item.quantity if item else 0

    def to_dict(self) -> dict:
        """Convierte la orden a diccionario para serialización"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "user_id": self.user_id,
            "status": self.status.value,
            "currency": self.currency.value,
            "shipping_address": self.shipping_address,
            "billing_address": self.billing_address,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "shipping_cost": float(self.shipping_cost),
            "discount_amount": float(self.discount_amount),
            "total_amount": float(self.total_amount),
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "product_sku": item.product_sku,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "total_price": float(item.total_price)
                }
                for item in self.items
            ],
            "status_history": [
                {
                    "status": h.status.value,
                    "comment": h.comment,
                    "created_at": h.created_at.isoformat() if h.created_at else None
                }
                for h in self.status_history
            ],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }