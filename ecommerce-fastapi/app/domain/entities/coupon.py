from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.domain.enums import DiscountType
from app.domain.exceptions import ValidationError, BusinessRuleException

@dataclass
class Coupon:
    id: Optional[int]
    code: str
    description: Optional[str] = None
    discount_type: DiscountType = DiscountType.PERCENTAGE
    discount_value: Decimal = Decimal("0")
    min_order_amount: Decimal = Decimal("0")
    max_uses: Optional[int] = None
    used_count: int = 0
    valid_from: datetime = field(default_factory=datetime.now)
    valid_until: Optional[datetime] = None
    is_active: bool = True

    def __post_init__(self):
        if not self.code or len(self.code.strip()) == 0:
            raise ValidationError("El código del cupón es obligatorio")
        if self.discount_value <= 0:
            raise ValidationError("El valor del descuento debe ser mayor a 0")
        if self.discount_type == DiscountType.PERCENTAGE and self.discount_value > 100:
            raise ValidationError("El descuento porcentual no puede exceder 100%")
        if self.min_order_amount < 0:
            raise ValidationError("El monto mínimo de orden no puede ser negativo")

    def is_valid(self, order_amount: Decimal) -> bool:
        """Verifica si el cupón es válido para una orden"""
        if not self.is_active:
            return False
        if self.valid_until and datetime.now() > self.valid_until:
            return False
        if datetime.now() < self.valid_from:
            return False
        if self.max_uses and self.used_count >= self.max_uses:
            return False
        if order_amount < self.min_order_amount:
            return False
        return True

    def use(self):
        """Incrementa el contador de usos"""
        if self.max_uses and self.used_count >= self.max_uses:
            raise BusinessRuleException("El cupón ha alcanzado su límite de usos")
        self.used_count += 1

    def calculate_discount(self, order_amount: Decimal) -> Decimal:
        """Calcula el monto del descuento"""
        if not self.is_valid(order_amount):
            return Decimal("0")
        
        if self.discount_type == DiscountType.PERCENTAGE:
            return (order_amount * self.discount_value) / 100
        else:
            return min(self.discount_value, order_amount)