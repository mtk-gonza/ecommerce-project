from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from app.domain.enums import ProductStatus, Currency

class SpecificationSchema(BaseModel):
    key: str
    value: str

class ProductImageSchema(BaseModel):
    id: Optional[int] = None
    url: str
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_main: bool = False

class ProductCreateSchema(BaseModel):
    sku: str = Field(..., max_length=50)
    slug: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    base_price: Decimal = Field(..., ge=0)
    currency: Currency = Currency.USD
    cost_price: Optional[Decimal] = Field(None, ge=0)
    discount_price: Optional[Decimal] = Field(None, ge=0)
    stock: int = Field(0, ge=0)
    low_stock_threshold: int = Field(5, ge=0)
    weight: Optional[Decimal] = None
    dimensions: Optional[str] = None
    status: ProductStatus = ProductStatus.ACTIVE
    is_visible: bool = True
    is_featured: bool = False
    category_id: Optional[int] = None
    specifications: List[SpecificationSchema] = []
    images: List[ProductImageSchema] = []

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    base_price: Optional[Decimal] = Field(None, ge=0)
    discount_price: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    status: Optional[ProductStatus] = None
    is_visible: Optional[bool] = None

class ProductSchema(BaseModel):
    id: int
    sku: str
    slug: str
    name: str
    description: Optional[str]
    base_price: Decimal
    currency: Currency
    cost_price: Optional[Decimal]
    discount_price: Optional[Decimal]
    stock: int
    low_stock_threshold: int
    weight: Optional[Decimal]
    dimensions: Optional[str]
    status: ProductStatus
    is_visible: bool
    is_featured: bool
    category_id: Optional[int]
    specifications: List[SpecificationSchema]
    images: List[ProductImageSchema]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)