from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from app.domain.enums import ProductStatus, Currency
from app.domain.exceptions import ValidationError, InvalidPriceException, InsufficientStockException

if TYPE_CHECKING:
    from app.domain.entities.category import Category

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
    # ==================== CAMPOS OBLIGATORIOS (sin default) ====================
    id: Optional[int]
    sku: str
    slug: str
    name: str
    base_price: Decimal
    
    # ==================== CAMPOS OPCIONALES (con default) ====================
    description: Optional[str] = None
    currency: Currency = Currency.ARS
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
    
    # Relaciones
    category: Optional['Category'] = None
    specifications: List[Specification] = field(default_factory=list)
    images: List[ProductImage] = field(default_factory=list)
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validaciones de negocio"""
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
        if not isinstance(self.currency, Currency):
            raise ValidationError("Moneda inválida")
        if self.discount_price is not None and self.discount_price > self.base_price:
            raise InvalidPriceException("El precio con descuento no puede ser mayor al precio base")

    # ==================== PROPIEDADES CALCULADAS ====================
    
    @property
    def final_price(self) -> Decimal:
        """Precio final (con descuento si aplica)"""
        return self.discount_price if self.discount_price else self.base_price

    @property
    def has_discount(self) -> bool:
        """¿Tiene descuento activo?"""
        return self.discount_price is not None and self.discount_price < self.base_price

    @property
    def discount_percentage(self) -> Decimal:
        """Porcentaje de descuento"""
        if not self.has_discount:
            return Decimal("0")
        return ((self.base_price - self.discount_price) / self.base_price) * 100

    @property
    def is_available(self) -> bool:
        """¿Está disponible para compra?"""
        return self.status == ProductStatus.ACTIVE and self.is_visible and self.stock > 0

    # ==================== MÉTODOS DE STOCK ====================
    
    def is_low_stock(self) -> bool:
        """¿Stock bajo según umbral?"""
        return self.stock <= self.low_stock_threshold

    def is_out_of_stock(self) -> bool:
        """¿Agotado?"""
        return self.stock <= 0

    def reduce_stock(self, quantity: int):
        """Reducir stock (para órdenes)"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        if self.stock < quantity:
            raise InsufficientStockException(f"Stock insuficiente. Disponible: {self.stock}")
        self.stock -= quantity
        self.updated_at = datetime.now()

    def increase_stock(self, quantity: int):
        """Aumentar stock (para cancelaciones o reposición)"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        self.stock += quantity
        self.updated_at = datetime.now()