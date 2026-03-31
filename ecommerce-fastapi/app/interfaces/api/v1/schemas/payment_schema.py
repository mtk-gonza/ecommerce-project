# interfaces/api/v1/schemas/payment_schema.py

from pydantic import BaseModel, Field, ConfigDict, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency

# ==================== PAYMENT CREATE ====================

class PaymentPreferenceCreateSchema(BaseModel):
    """Schema para crear preferencia de pago (checkout con redirección)"""
    order_id: int = Field(..., ge=1)
    payer_email: str = Field(..., min_length=5, max_length=150)
    payer_name: Optional[str] = Field(None, max_length=100)
    payer_identification: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)

class PaymentDirectCreateSchema(BaseModel):
    """Schema para crear pago directo con tarjeta"""
    order_id: int = Field(..., ge=1)
    token: str = Field(..., min_length=10)  # Token de MercadoPago.js
    payment_method_id: str = Field(..., min_length=3)  # "visa", "mastercard", etc.
    installments: int = Field(default=1, ge=1, le=24)
    issuer_id: Optional[str] = None
    payer_email: str = Field(..., min_length=5, max_length=150)
    payer_name: Optional[str] = Field(None, max_length=100)
    payer_identification: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)

# ==================== PAYMENT RESPONSE ====================

class PaymentSchema(BaseModel):
    """Schema completo de respuesta para pago"""
    id: int
    order_id: int
    external_id: Optional[str]
    provider: str
    amount: Decimal
    currency: str
    status: str
    payment_method_type: Optional[str]
    payer_email: Optional[str]
    payer_name: Optional[str]
    mp_payment_id: Optional[str]
    mp_card_last_four: Optional[str]
    mp_installments: Optional[int]
    date_approved: Optional[datetime]
    date_created: Optional[datetime]
    is_completed: bool
    is_pending: bool
    can_be_refunded: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentPreferenceResponseSchema(BaseModel):
    """Respuesta para creación de preferencia"""
    success: bool
    payment_id: int
    preference_id: str
    init_point: str  # URL para redirigir al usuario
    amount: Decimal
    currency: str
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentDirectResponseSchema(BaseModel):
    """Respuesta para pago directo"""
    success: bool
    payment_id: int
    mp_payment_id: str
    status: str
    message: str

    model_config = ConfigDict(from_attributes=True)

# ==================== PAYMENT ACTIONS ====================

class PaymentRefundSchema(BaseModel):
    """Schema para procesar reembolso"""
    amount: Optional[Decimal] = Field(None, ge=0)
    reason: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)

class PaymentCancelSchema(BaseModel):
    """Schema para cancelar pago"""
    reason: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)

# ==================== WEBHOOK ====================

class WebhookNotificationSchema(BaseModel):
    """Schema para notificaciones webhook de MercadoPago"""
    action: str  # "payment.created", "payment.updated", etc.
    api_version: str
    data: Dict[str, Any]
    date_created: datetime
    id: int
    live_mode: bool
    type: str  # "payment", "merchant_order", etc.
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# ==================== RESPONSES WRAPPER ====================

class PaymentResponseSchema(BaseModel):
    """Respuesta estándar para operaciones de pago"""
    success: bool
    message: str
    payment: Optional[PaymentSchema] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentMethodsResponseSchema(BaseModel):
    """Respuesta para lista de métodos de pago"""
    success: bool
    methods: List[Dict[str, str]]
    country: str

    model_config = ConfigDict(from_attributes=True)