from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from app.domain.enums import PaymentStatus
from sqlalchemy.sql import func

class PaymentMethodModel(Base, TimestampMixin):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, nullable=False)  # 'card', 'paypal', 'transfer'
    is_active = Column(Boolean, default=True)

    # ==================== RELACIONES ====================
    payments = relationship(
        "PaymentModel",
        back_populates="payment_method",
        lazy="select"
    )


class PaymentModel(Base, TimestampMixin):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=False)
    
    transaction_id = Column(String(100), nullable=True, index=True)
    
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    # ==================== RELACIONES ====================
    order = relationship(
        "OrderModel",
        back_populates="payments"
    )
    payment_method = relationship(
        "PaymentMethodModel",
        back_populates="payments"
    )

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status='{self.status.value}')>"


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