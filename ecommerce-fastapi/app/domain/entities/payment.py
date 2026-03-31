# domain/entities/payment.py

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency
from app.domain.exceptions import ValidationError, BusinessRuleException

@dataclass
class Payment:
    """
    Entidad de Pago - Representa una transacción de pago procesada
    """
    # ==================== CAMPOS OBLIGATORIOS ====================
    id: Optional[int]
    order_id: int
    external_id: Optional[str] = None  # ID de pago en MercadoPago
    provider: PaymentProvider = PaymentProvider.MERCADOPAGO
    
    # ==================== CAMPOS CON DEFAULT ====================
    amount: Decimal = Decimal("0")
    currency: Currency = Currency.USD
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method_type: Optional[PaymentMethodType] = None
    
    # Datos del pagador (snapshot)
    payer_email: Optional[str] = None
    payer_name: Optional[str] = None
    payer_identification: Optional[str] = None  # DNI/CUIT para algunos métodos
    
    # Metadata de MercadoPago
    mp_payment_id: Optional[str] = None  # ID interno de MercadoPago
    mp_transaction_amount: Optional[Decimal] = None
    mp_installments: Optional[int] = None
    mp_payment_method_id: Optional[str] = None  # ID del método (visa, mastercard, etc.)
    mp_issuer_id: Optional[str] = None  # ID del banco emisor
    mp_card_last_four: Optional[str] = None  # Últimos 4 dígitos de la tarjeta
    
    # Fechas importantes
    date_approved: Optional[datetime] = None
    date_created: Optional[datetime] = None
    date_last_updated: Optional[datetime] = None
    
    # Metadata adicional
    description: Optional[str] = None
    statement_descriptor: Optional[str] = None  # Texto que aparece en el extracto
    notification_url: Optional[str] = None  # Webhook URL para notificaciones
    back_urls: dict = field(default_factory=lambda: {"success": "", "pending": "", "failure": ""})
    
    # Intentos y errores
    attempts: int = 0
    last_error: Optional[str] = None
    last_error_code: Optional[str] = None
    
    # Auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validaciones de negocio"""
        if not self.order_id:
            raise ValidationError("El order_id es obligatorio")
        if self.amount <= 0:
            raise ValidationError("El monto debe ser mayor a 0")
        if not isinstance(self.status, PaymentStatus):
            raise ValidationError("Estado de pago inválido")
        if not isinstance(self.provider, PaymentProvider):
            raise ValidationError("Proveedor de pago inválido")
        if self.currency not in [Currency.ARS, Currency.BRL, Currency.MXN, Currency.COP, Currency.CLP, Currency.PEN, Currency.UYU, Currency.USD]:
            raise ValidationError(f"Moneda no soportada por MercadoPago: {self.currency.value}")

    # ==================== PROPIEDADES ====================
    
    @property
    def is_completed(self) -> bool:
        """¿El pago está completado exitosamente?"""
        return self.status == PaymentStatus.APPROVED

    @property
    def is_pending(self) -> bool:
        """¿El pago está pendiente de confirmación?"""
        return self.status in [PaymentStatus.PENDING, PaymentStatus.IN_PROCESS, PaymentStatus.AUTHORIZED]

    @property
    def is_failed(self) -> bool:
        """¿El pago falló o fue rechazado?"""
        return self.status in [PaymentStatus.REJECTED, PaymentStatus.CANCELLED, PaymentStatus.CHARGEBACK]

    @property
    def can_be_refunded(self) -> bool:
        """¿Se puede reembolsar este pago?"""
        return self.status == PaymentStatus.APPROVED

    @property
    def requires_action(self) -> bool:
        """¿Requiere acción del usuario (ej: pagar en efectivo)?"""
        return self.status in [PaymentStatus.PENDING, PaymentStatus.AUTHORIZED] and self.payment_method_type == PaymentMethodType.TICKET

    # ==================== MÉTODOS DE ESTADO ====================
    
    def approve(self, mp_payment_id: str, transaction_amount: Decimal, 
                payment_method_id: Optional[str] = None, card_last_four: Optional[str] = None):
        """Aprueba el pago con datos de MercadoPago"""
        if self.status != PaymentStatus.PENDING:
            raise BusinessRuleException(f"No se puede aprobar un pago en estado '{self.status.value}'")
        
        self.status = PaymentStatus.APPROVED
        self.mp_payment_id = mp_payment_id
        self.mp_transaction_amount = transaction_amount
        self.mp_payment_method_id = payment_method_id
        self.mp_card_last_four = card_last_four
        self.date_approved = datetime.now()
        self.date_last_updated = datetime.now()

    def reject(self, error_code: Optional[str] = None, error_message: Optional[str] = None):
        """Rechaza el pago"""
        self.status = PaymentStatus.REJECTED
        self.last_error_code = error_code
        self.last_error = error_message
        self.date_last_updated = datetime.now()
        self.attempts += 1

    def cancel(self, reason: Optional[str] = None):
        """Cancela el pago por solicitud del usuario"""
        if self.status not in [PaymentStatus.PENDING, PaymentStatus.AUTHORIZED]:
            raise BusinessRuleException(f"No se puede cancelar un pago en estado '{self.status.value}'")
        
        self.status = PaymentStatus.CANCELLED
        self.last_error = reason
        self.date_last_updated = datetime.now()

    def refund(self, amount: Optional[Decimal] = None):
        """Procesa un reembolso (total o parcial)"""
        if not self.can_be_refunded:
            raise BusinessRuleException(f"No se puede reembolsar un pago en estado '{self.status.value}'")
        
        refund_amount = amount if amount else self.amount
        if refund_amount > self.amount:
            raise ValidationError("El monto del reembolso no puede ser mayor al pago original")
        
        self.status = PaymentStatus.REFUNDED
        self.date_last_updated = datetime.now()
        # Nota: El reembolso real se procesa vía API de MercadoPago

    def update_from_mercadopago(self, mp_data: dict):
        """
        Actualiza el pago con datos del webhook de MercadoPago.
        mp_data: dict con la respuesta de la API de MercadoPago
        """
        # Mapear estados de MercadoPago a nuestros estados
        mp_status = mp_data.get("status", "").lower()
        status_mapping = {
            "pending": PaymentStatus.PENDING,
            "approved": PaymentStatus.APPROVED,
            "authorized": PaymentStatus.AUTHORIZED,
            "in_process": PaymentStatus.IN_PROCESS,
            "in_mediation": PaymentStatus.PENDING,
            "rejected": PaymentStatus.REJECTED,
            "cancelled": PaymentStatus.CANCELLED,
            "refunded": PaymentStatus.REFUNDED,
            "charged_back": PaymentStatus.CHARGEBACK,
        }
        
        self.status = status_mapping.get(mp_status, PaymentStatus.UNKNOWN)
        self.mp_payment_id = str(mp_data.get("id", ""))
        self.mp_transaction_amount = Decimal(str(mp_data.get("transaction_amount", self.amount)))
        self.mp_payment_method_id = mp_data.get("payment_method_id")
        self.mp_issuer_id = mp_data.get("issuer_id")
        self.mp_installments = mp_data.get("installments")
        
        # Datos del pagador
        payer = mp_data.get("payer", {})
        self.payer_email = payer.get("email") or self.payer_email
        self.payer_name = payer.get("identification", {}).get("number") or self.payer_identification
        
        # Fechas
        if mp_data.get("date_approved"):
            self.date_approved = datetime.fromisoformat(mp_data["date_approved"].replace("Z", "+00:00"))
        if mp_data.get("date_created"):
            self.date_created = datetime.fromisoformat(mp_data["date_created"].replace("Z", "+00:00"))
        
        self.date_last_updated = datetime.now()

    def to_dict(self) -> dict:
        """Convierte el pago a diccionario para serialización"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "external_id": self.external_id,
            "provider": self.provider.value,
            "amount": float(self.amount),
            "currency": self.currency.value,
            "status": self.status.value,
            "payment_method_type": self.payment_method_type.value if self.payment_method_type else None,
            "payer_email": self.payer_email,
            "payer_name": self.payer_name,
            "mp_payment_id": self.mp_payment_id,
            "mp_card_last_four": self.mp_card_last_four,
            "mp_installments": self.mp_installments,
            "date_approved": self.date_approved.isoformat() if self.date_approved else None,
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "is_completed": self.is_completed,
            "is_pending": self.is_pending,
            "can_be_refunded": self.can_be_refunded,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }