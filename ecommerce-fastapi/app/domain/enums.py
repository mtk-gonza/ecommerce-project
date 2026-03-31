from enum import Enum, auto

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"

class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"
    ARCHIVED = "archived"

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    ARS = "ARS"
    MXN = "MXN"
    COP = "COP"
    BRL = "BRL"
    CLP = "CLP"
    PEN = "PEN"
    UYU = "UYU"

class AddressType(Enum):
    BILLING = "billing"
    SHIPPING = "shipping"
    BOTH = "both"

class DiscountType(Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PaymentStatus(str, Enum):
    """Estados de pago de MercadoPago"""
    PENDING = "pending"        # Pago iniciado, esperando confirmación
    APPROVED = "approved"      # Pago aprobado y confirmado
    AUTHORIZED = "authorized"  # Pago autorizado (para capturar después)
    IN_PROCESS = "in_process"  # Pago en proceso de revisión
    REJECTED = "rejected"      # Pago rechazado
    REFUNDED = "refunded"      # Pago reembolsado
    CANCELLED = "cancelled"    # Pago cancelado por usuario
    CHARGEBACK = "chargeback"  # Contracargo iniciado
    UNKNOWN = "unknown"        # Estado desconocido

class PaymentMethodType(str, Enum):
    """Tipos de método de pago soportados"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ACCOUNT_MONEY = "account_money"  # Saldo en cuenta MercadoPago
    TICKET = "ticket"          # Pago en efectivo (Rapipago, Oxxo, etc.)
    BANK_TRANSFER = "bank_transfer"
    ATM = "atm"

class PaymentProvider(str, Enum):
    """Proveedores de pago soportados"""
    MERCADOPAGO = "mercadopago"
    # Futuros: STRIPE = "stripe", PAYPAL = "paypal"