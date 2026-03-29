from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from app.domain.enums import OrderStatus, Currency

class OrderItemCreateSchema(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)

class OrderCreateSchema(BaseModel):
    shipping_address: str
    billing_address: str
    items: List[OrderItemCreateSchema]
    notes: Optional[str] = None

class OrderItemSchema(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderSchema(BaseModel):
    id: int
    order_number: str
    user_id: int
    status: OrderStatus
    currency: Currency
    shipping_address: str
    billing_address: str
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    items: List[OrderItemSchema]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)