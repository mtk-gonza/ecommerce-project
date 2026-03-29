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

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    ARS = "ARS"
    MXN = "MXN"
    COP = "COP"
    BRL = "BRL"

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