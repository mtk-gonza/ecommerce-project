# interfaces/api/v1/schemas/order_schema.py

from pydantic import BaseModel, Field, ConfigDict, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from app.domain.enums import OrderStatus, Currency

# ==================== ORDER ITEM ====================

class OrderItemCreateSchema(BaseModel):
    """Schema para crear item de orden"""
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1, le=999)

    model_config = ConfigDict(from_attributes=True)

class OrderItemSchema(BaseModel):
    """Schema de respuesta para item de orden"""
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)

# ==================== ORDER STATUS HISTORY ====================

class OrderStatusHistorySchema(BaseModel):
    """Schema para historial de estados"""
    status: str
    comment: Optional[str] = None
    created_at: datetime
    commented_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# ==================== ORDER CREATE ====================

class OrderCreateFromCartSchema(BaseModel):
    """Schema para crear orden desde carrito"""
    cart_id: int = Field(..., ge=1)
    shipping_address: str = Field(..., min_length=10)
    billing_address: str = Field(..., min_length=10)
    notes: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

class OrderCreateDirectSchema(BaseModel):
    """Schema para crear orden directamente (sin carrito)"""
    items: List[OrderItemCreateSchema] = Field(..., min_length=1)
    shipping_address: str = Field(..., min_length=10)
    billing_address: str = Field(..., min_length=10)
    notes: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

# ==================== ORDER RESPONSE ====================

class OrderSchema(BaseModel):
    """Schema completo de respuesta para orden"""
    id: int
    order_number: str
    user_id: int
    status: str
    currency: str
    shipping_address: str
    billing_address: str
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    items: List[OrderItemSchema]
    status_history: List[OrderStatusHistorySchema]
    notes: Optional[str] = None
    payment_reference: Optional[str] = None
    total_items: int
    unique_items: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderSummarySchema(BaseModel):
    """Schema resumido para listas de órdenes"""
    id: int
    order_number: str
    status: str
    total_amount: Decimal
    total_items: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ==================== ORDER ACTIONS ====================

class OrderStatusUpdateSchema(BaseModel):
    """Schema para actualizar estado de orden"""
    new_status: OrderStatus
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class OrderCancelSchema(BaseModel):
    """Schema para cancelar orden"""
    reason: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

class OrderShipSchema(BaseModel):
    """Schema para marcar orden como enviada"""
    tracking_number: Optional[str] = Field(None, max_length=100)

    model_config = ConfigDict(from_attributes=True)

class OrderRefundSchema(BaseModel):
    """Schema para procesar reembolso"""
    amount: Optional[Decimal] = Field(None, ge=0)
    reason: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

# ==================== RESPONSES WRAPPER ====================

class OrderResponseSchema(BaseModel):
    """Respuesta estándar para operaciones de orden"""
    success: bool
    message: str
    order: Optional[OrderSchema] = None

    model_config = ConfigDict(from_attributes=True)

class OrdersListResponseSchema(BaseModel):
    """Respuesta para lista de órdenes"""
    success: bool
    message: str
    orders: List[OrderSummarySchema]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)

class OrderStatsSchema(BaseModel):
    """Respuesta para estadísticas de órdenes"""
    total_orders: int
    total_sales: float
    status_breakdown: dict
    average_order_value: float

    model_config = ConfigDict(from_attributes=True)