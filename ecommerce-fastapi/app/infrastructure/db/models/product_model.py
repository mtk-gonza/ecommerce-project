from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from app.domain.enums import ProductStatus, Currency
from sqlalchemy.sql import func

class ProductModel(Base, TimestampMixin):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD)
    cost_price = Column(Numeric(10, 2), nullable=True)
    discount_price = Column(Numeric(10, 2), nullable=True)
    stock = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=5)
    weight = Column(Numeric(8, 2), nullable=True)
    dimensions = Column(String(50), nullable=True)
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    is_visible = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    # ==================== RELACIONES ====================
    category = relationship("CategoryModel", back_populates="products")
    images = relationship(
        "ProductImageModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select"
    )
    specifications = relationship(
        "ProductSpecificationModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select"
    )
    reviews = relationship(
        "ReviewModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select"
    )
    wishlists = relationship(
        "WishlistModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select"
    )
    cart_items = relationship(
        "CartItemModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select"
    )
    order_items = relationship(
        "OrderItemModel",
        back_populates="product",
        lazy="select"
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"


class ProductImageModel(Base, TimestampMixin):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    url = Column(String(255), nullable=False)
    alt_text = Column(String(100), nullable=True)
    sort_order = Column(Integer, default=0)
    is_main = Column(Boolean, default=False)

    product = relationship("ProductModel", back_populates="images")


class ProductSpecificationModel(Base, TimestampMixin):
    __tablename__ = 'product_specifications'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)

    product = relationship("ProductModel", back_populates="specifications")