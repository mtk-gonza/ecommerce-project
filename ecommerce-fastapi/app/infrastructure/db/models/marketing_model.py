from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, DateTime, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base, TimestampMixin

class CouponModel(Base, TimestampMixin):
    __tablename__ = 'coupons'
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    discount_type = Column(Enum('percent', 'fixed'), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    min_order_amount = Column(Numeric(10, 2), default=0.00)
    max_uses = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
    valid_from = Column(DateTime(timezone=True), server_default=func.now())
    valid_until = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

class ReviewModel(Base, TimestampMixin):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
    rating = Column(Integer, nullable=False)
    title = Column(String(100))
    comment = Column(Text)
    is_approved = Column(Boolean, default=False)
    
    product = relationship("ProductModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews")
    order = relationship("OrderModel")
    
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

class WishlistModel(Base, TimestampMixin):
    __tablename__ = 'wishlists'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship("UserModel", back_populates="wishlists")
    product = relationship("ProductModel", back_populates="wishlists")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='unique_wishlist'),
    )