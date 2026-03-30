from pydantic import BaseModel, Field, ConfigDict, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from app.domain.enums import ProductStatus, Currency

# ==================== ESPECIFICACIONES ====================

class SpecificationBase(BaseModel):
    key: str = Field(..., min_length=2, max_length=100)
    value: str = Field(..., min_length=1, max_length=255)

class SpecificationCreateSchema(SpecificationBase):
    pass

class SpecificationSchema(SpecificationBase):
    model_config = ConfigDict(from_attributes=True)

# ==================== IMÁGENES ====================

class ProductImageBase(BaseModel):
    url: str = Field(..., min_length=10, max_length=500)
    alt_text: Optional[str] = Field(None, max_length=200)
    sort_order: int = Field(default=0, ge=0)
    is_main: bool = False

class ProductImageCreateSchema(ProductImageBase):
    pass

class ProductImageSchema(ProductImageBase):
    id: Optional[int] = None
    product_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

# ==================== PRODUCTO - BASE ====================

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50, pattern=r'^[A-Z0-9\-]+$')
    slug: Optional[str] = Field(None, min_length=3, max_length=220, pattern=r'^[a-z0-9\-]+$')
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    short_description: Optional[str] = Field(None, max_length=500)
    base_price: Decimal = Field(..., ge=0, le=999999.99)
    currency: Currency = Currency.USD
    cost_price: Optional[Decimal] = Field(None, ge=0)
    discount_price: Optional[Decimal] = Field(None, ge=0)
    stock: int = Field(default=0, ge=0, le=999999)
    low_stock_threshold: int = Field(default=5, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=50)
    status: ProductStatus = ProductStatus.ACTIVE
    is_visible: bool = True
    is_featured: bool = False
    category_id: Optional[int] = None

    @field_validator('discount_price')
    @classmethod
    def discount_must_be_less_than_base(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        if v is not None and 'base_price' in info.data and v > info.data['base_price']:
            raise ValueError('El precio con descuento no puede ser mayor al precio base')
        return v

# ==================== PRODUCTO - CREATE ====================

class ProductCreateSchema(ProductBase):
    specifications: List[SpecificationCreateSchema] = Field(default_factory=list)
    images: List[ProductImageCreateSchema] = Field(default_factory=list)

# ==================== PRODUCTO - UPDATE ====================

class ProductUpdateSchema(BaseModel):
    """Schema para actualización parcial - todos los campos son opcionales"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    short_description: Optional[str] = Field(None, max_length=500)
    base_price: Optional[Decimal] = Field(None, ge=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    discount_price: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=50)
    status: Optional[ProductStatus] = None
    is_visible: Optional[bool] = None
    is_featured: Optional[bool] = None
    category_id: Optional[int] = None

    @field_validator('discount_price')
    @classmethod
    def discount_must_be_less_than_base(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        if v is not None and 'base_price' in info.data and info.data['base_price'] is not None and v > info.data['base_price']:
            raise ValueError('El precio con descuento no puede ser mayor al precio base')
        return v

# ==================== PRODUCTO - RESPONSE ====================

class ProductSchema(ProductBase):
    id: int
    specifications: List[SpecificationSchema] = Field(default_factory=list)
    images: List[ProductImageSchema] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Campos calculados (solo lectura)
    final_price: Decimal = Field(..., exclude=True)
    has_discount: bool = Field(..., exclude=True)
    discount_percentage: Optional[Decimal] = Field(None, exclude=True)
    is_available: bool = Field(..., exclude=True)
    is_low_stock: bool = Field(..., exclude=True)
    is_out_of_stock: bool = Field(..., exclude=True)

    model_config = ConfigDict(from_attributes=True)

# ==================== RESPONSES WRAPPER ====================

class ProductResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[ProductSchema] = None
    model_config = ConfigDict(from_attributes=True)

class ProductsListResponseSchema(BaseModel):
    success: bool
    message: str
    data: List[ProductSchema]
    total: int
    skip: int
    limit: int
    model_config = ConfigDict(from_attributes=True)

class ProductStatsSchema(BaseModel):
    total_products: int
    active_products: int
    low_stock_products: int
    out_of_stock_products: int
    featured_products: int
    total_inventory_value: Decimal
    model_config = ConfigDict(from_attributes=True)