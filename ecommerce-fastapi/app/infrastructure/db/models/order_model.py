from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from app.domain.enums import OrderStatus, Currency
from sqlalchemy.sql import func

class OrderModel(Base, TimestampMixin):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    currency = Column(Enum(Currency), default=Currency.USD)
    
    # Snapshot de direcciones (texto plano para historial)
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    
    # Montos
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0.00)
    shipping_cost = Column(Numeric(10, 2), default=0.00)
    discount_amount = Column(Numeric(10, 2), default=0.00)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    notes = Column(Text, nullable=True)

    # ==================== RELACIONES ====================
    user = relationship("UserModel", back_populates="orders")
    items = relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="select"
    )
    status_history = relationship(
        "OrderStatusHistoryModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="select"
    )
    payments = relationship(
        "PaymentModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="select"
    )
    shipments = relationship(
        "ShipmentModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __repr__(self):
        return f"<Order(id={self.id}, number='{self.order_number}', status='{self.status.value}')>"


class OrderItemModel(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    # Snapshot del producto al momento de la compra
    product_name = Column(String(200), nullable=False)
    product_sku = Column(String(50), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    # ==================== RELACIONES ====================
    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel", back_populates="order_items")


class OrderStatusHistoryModel(Base):
    __tablename__ = 'order_status_history'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    
    commented_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    comment = Column(Text, nullable=True)
    

    # ==================== RELACIONES ====================
    order = relationship("OrderModel", back_populates="status_history")
    commenter = relationship("UserModel", foreign_keys=[commented_by])

    def __repr__(self):
        return f"<OrderStatusHistory(order_id={self.order_id}, status='{self.status.value}')>"