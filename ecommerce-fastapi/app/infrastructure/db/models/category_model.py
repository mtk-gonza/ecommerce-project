from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base, TimestampMixin
from sqlalchemy.sql import func

class CategoryModel(Base, TimestampMixin):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relación recursiva para subcategorías
    parent = relationship(
        "CategoryModel",
        remote_side=[id],
        backref="subcategories"
    )
    
    # Relación con productos
    products = relationship("ProductModel", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', slug='{self.slug}')>"