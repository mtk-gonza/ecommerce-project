from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from app.domain.enums import ProductStatus, Currency
from app.domain.exceptions import ValidationError, InvalidPriceException, InsufficientStockException

@dataclass
class Specification:
    key: str
    value: str

@dataclass
class ProductImage:
    id: Optional[int]
    url: str
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_main: bool = False

@dataclass
class Product:
    id: Optional[int]
    sku: str
    slug: str
    name: str
    description: Optional[str]
    base_price: Decimal
    currency: Currency = Currency.USD
    cost_price: Optional[Decimal] = None
    discount_price: Optional[Decimal] = None
    stock: int = 0
    low_stock_threshold: int = 5
    weight: Optional[Decimal] = None
    dimensions: Optional[str] = None
    status: ProductStatus = ProductStatus.ACTIVE
    is_visible: bool = True
    is_featured: bool = False
    category_id: Optional[int] = None
    specifications: List[Specification] = field(default_factory=list)
    images: List[ProductImage] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        if not self.sku or len(self.sku.strip()) == 0:
            raise ValidationError("El SKU es obligatorio")
        if not self.slug or len(self.slug.strip()) == 0:
            raise ValidationError("El slug es obligatorio")
        if self.base_price < 0:
            raise InvalidPriceException("El precio base no puede ser negativo")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo")
        if not isinstance(self.status, ProductStatus):
            raise ValidationError("Estado de producto inválido")

    @property
    def final_price(self) -> Decimal:
        return self.discount_price if self.discount_price else self.base_price

    @property
    def has_discount(self) -> bool:
        return self.discount_price is not None and self.discount_price < self.base_price

    @property
    def is_available(self) -> bool:
        return self.status == ProductStatus.ACTIVE and self.is_visible and self.stock > 0

    def reduce_stock(self, quantity: int):
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        if self.stock < quantity:
            raise InsufficientStockException(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= quantity
        self.updated_at = datetime.now()

    def increase_stock(self, quantity: int):
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        self.stock += quantity
        self.updated_at = datetime.now()