from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from app.domain.exceptions import ValidationError, InsufficientStockException

@dataclass
class CartItem:
    id: Optional[int]
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity

@dataclass
class Cart:
    id: Optional[int]
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    items: List[CartItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.user_id and not self.session_id:
            raise ValidationError("El carrito debe tener user_id o session_id")

    @property
    def subtotal(self) -> Decimal:
        return sum(item.total_price for item in self.items)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    def add_item(self, product_id: int, product_name: str, product_sku: str, quantity: int, unit_price: Decimal):
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                self.updated_at = datetime.now()
                return
        self.items.append(CartItem(id=None, product_id=product_id, product_name=product_name, product_sku=product_sku, quantity=quantity, unit_price=unit_price))
        self.updated_at = datetime.now()

    def remove_item(self, product_id: int):
        self.items = [item for item in self.items if item.product_id != product_id]
        self.updated_at = datetime.now()

    def clear(self):
        self.items = []
        self.updated_at = datetime.now()

    def is_empty(self) -> bool:
        return len(self.items) == 0