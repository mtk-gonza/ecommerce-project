from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency
from sqlalchemy.sql import func

class PaymentMethodModel(Base, TimestampMixin):
    """
    Métodos de pago disponibles (configuración estática).
    Ej: Visa, Mastercard, RapiPago, Transferencia, etc.
    """
    __tablename__ = 'payment_methods'
    
    __allow_unmapped__ = True  # Para compatibilidad con SQLAlchemy 2.0
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # "Visa", "Mastercard", "RapiPago"
    code = Column(String(50), unique=True, nullable=False)  # "visa", "master", "rapipago"
    type = Column(Enum(PaymentMethodType), nullable=False)  # credit_card, ticket, etc.
    provider = Column(Enum(PaymentProvider), default=PaymentProvider.MERCADOPAGO)
    is_active = Column(Boolean, default=True)
    min_amount = Column(Numeric(10, 2), nullable=True)  # Monto mínimo para usar este método
    max_amount = Column(Numeric(10, 2), nullable=True)  # Monto máximo
    countries = Column(Text, nullable=True)  # JSON: ["AR", "BR", "MX"]
    
    # ==================== RELACIONES ====================
    # ✅ back_populates debe coincidir EXACTAMENTE con el nombre en PaymentModel
    payments = relationship(
        "PaymentModel",
        back_populates="payment_method",
        lazy="select"
    )


class PaymentModel(Base, TimestampMixin):
    """
    Transacción de pago procesada.
    """
    __tablename__ = 'payments'
    
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    
    # IDs externos
    external_id = Column(String(100), unique=True, nullable=True, index=True)
    mp_payment_id = Column(String(100), nullable=True, index=True)
    
    # Proveedor y método
    provider = Column(Enum(PaymentProvider), default=PaymentProvider.MERCADOPAGO)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)  # ✅ FK hacia payment_methods
    payment_method_type = Column(Enum(PaymentMethodType), nullable=True)
    
    # Monto y moneda
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD)
    
    # Estado del pago
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Datos del pagador (snapshot)
    payer_email = Column(String(150), nullable=True)
    payer_name = Column(String(100), nullable=True)
    payer_identification = Column(String(50), nullable=True)
    
    # Metadata de MercadoPago
    mp_transaction_amount = Column(Numeric(10, 2), nullable=True)
    mp_installments = Column(Integer, nullable=True)
    mp_payment_method_id = Column(String(50), nullable=True)  # ID interno de MP (ej: "visa")
    mp_issuer_id = Column(String(50), nullable=True)
    mp_card_last_four = Column(String(4), nullable=True)
    
    # Fechas importantes
    date_approved = Column(DateTime(timezone=True), nullable=True)
    date_created = Column(DateTime(timezone=True), nullable=True)
    date_last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata adicional
    description = Column(String(255), nullable=True)
    statement_descriptor = Column(String(25), nullable=True)
    notification_url = Column(String(255), nullable=True)
    back_urls = Column(Text, nullable=True)  # JSON string
    
    # Intentos y errores
    attempts = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    last_error_code = Column(String(50), nullable=True)
    
    # ==================== RELACIONES ====================
    
    # ✅ Relación con Order
    order = relationship(
        "OrderModel",
        back_populates="payments",
        lazy="select"
    )
    
    # ✅ Relación con PaymentMethod (back_populates coincide con PaymentMethodModel.payments)
    payment_method = relationship(
        "PaymentMethodModel",
        back_populates="payments",
        lazy="select"
    )

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status='{self.status.value}', amount={self.amount})>"


class ShippingMethodModel(Base, TimestampMixin):
    __tablename__ = 'shipping_methods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cost = Column(Numeric(10, 2), default=0.00)
    min_days = Column(Integer, nullable=True)
    max_days = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    # ==================== RELACIONES ====================
    shipments = relationship(
        "ShipmentModel",
        back_populates="shipping_method",
        lazy="select"
    )


class ShipmentModel(Base, TimestampMixin):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    shipping_method_id = Column(Integer, ForeignKey('shipping_methods.id', ondelete='SET NULL'), nullable=True)
    
    tracking_number = Column(String(100), nullable=True, index=True)
    carrier = Column(String(100), nullable=True)
    
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # ==================== RELACIONES ====================
    order = relationship(
        "OrderModel",
        back_populates="shipments"
    )
    shipping_method = relationship(
        "ShippingMethodModel",
        back_populates="shipments"
    )

    def __repr__(self):
        return f"<Shipment(id={self.id}, order_id={self.order_id}, tracking='{self.tracking_number}')>"