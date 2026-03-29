from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from app.domain.enums import UserRole, AddressType
from sqlalchemy.sql import func


class UserModel(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)

    addresses = relationship("AddressModel", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("OrderModel", back_populates="user")
    cart = relationship("CartModel", back_populates="user", uselist=False)
    reviews = relationship("ReviewModel", back_populates="user")
    wishlists = relationship("WishlistModel", back_populates="user")


class AddressModel(Base, TimestampMixin):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    address_type = Column(Enum(AddressType), default=AddressType.BOTH)
    alias = Column(String(50), nullable=True)
    is_default = Column(Boolean, default=False)
    user = relationship("UserModel", back_populates="addresses")