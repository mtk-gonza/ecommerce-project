# interfaces/api/v1/schemas/cart_schema.py

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional, List

# ==================== CART ITEM ====================

class CartItemCreateSchema(BaseModel):
    """Schema para agregar item al carrito"""
    product_id: int = Field(..., ge=1)
    quantity: int = Field(default=1, ge=1, le=999)

    model_config = ConfigDict(from_attributes=True)

class CartItemUpdateSchema(BaseModel):
    """Schema para actualizar cantidad de item"""
    quantity: int = Field(..., ge=1, le=999)

    model_config = ConfigDict(from_attributes=True)

class CartItemSchema(BaseModel):
    """Schema de respuesta para item del carrito"""
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal  # quantity * unit_price

    model_config = ConfigDict(from_attributes=True)

# ==================== CART ====================

class CartCreateSchema(BaseModel):
    """Schema para crear carrito (interno)"""
    user_id: Optional[int] = None
    session_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CartAddItemSchema(BaseModel):
    """Schema para agregar item al carrito"""
    product_id: int
    quantity: int = Field(default=1, ge=1)

    model_config = ConfigDict(from_attributes=True)

class CartResponseSchema(BaseModel):
    """Schema de respuesta para carrito completo"""
    id: Optional[int]
    user_id: Optional[int]
    session_id: Optional[str]
    items: List[CartItemSchema]
    subtotal: Decimal
    total_items: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class CartSummarySchema(BaseModel):
    """Schema para resumen del carrito (checkout)"""
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total: Decimal
    items_count: int
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)

class CartMergeSchema(BaseModel):
    """Schema para merge de carrito de invitado a usuario"""
    session_id: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# ==================== RESPONSES WRAPPER ====================

class CartOperationResponseSchema(BaseModel):
    """Respuesta estándar para operaciones del carrito"""
    success: bool
    message: str
    data: Optional[CartResponseSchema] = None
    summary: Optional[CartSummarySchema] = None

    model_config = ConfigDict(from_attributes=True)