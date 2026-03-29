from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin

class CartModel(Base, TimestampMixin):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)

    # Relationships
    user = relationship("UserModel", back_populates="cart")
    items = relationship("CartItemModel", back_populates="cart", cascade="all, delete-orphan")

class CartItemModel(Base, TimestampMixin):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    product_name = Column(String(200), nullable=False)
    product_sku = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Integer, nullable=False)  # Guardar en centavos o usar Numeric

    # Relationships
    cart = relationship("CartModel", back_populates="items")
    product = relationship("ProductModel", back_populates="cart_items")