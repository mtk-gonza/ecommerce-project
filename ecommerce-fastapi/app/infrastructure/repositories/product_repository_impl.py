from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.domain.entities.product import Product
from app.domain.ports.product_repository import ProductRepositoryPort
from app.infrastructure.db.models.product_model import ProductModel
from app.infrastructure.mappers.product_mapper import ProductMapper
from app.domain.exceptions import EntityNotFoundException

class ProductRepositoryImpl(ProductRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, product: Product) -> Product:
        model = ProductMapper.to_model(product)
        if product.id:
            self.db.merge(model)
        else:
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return ProductMapper.to_entity(model)

    def find_by_id(self, product_id: int) -> Optional[Product]:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return ProductMapper.to_entity(model) if model else None

    def find_by_sku(self, sku: str) -> Optional[Product]:
        model = self.db.query(ProductModel).filter(ProductModel.sku == sku).first()
        return ProductMapper.to_entity(model) if model else None

    def find_by_slug(self, slug: str) -> Optional[Product]:
        model = self.db.query(ProductModel).filter(ProductModel.slug == slug).first()
        return ProductMapper.to_entity(model) if model else None

    def find_all(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
        query = self.db.query(ProductModel)
        if category_id:
            query = query.filter(ProductModel.category_id == category_id)
        models = query.offset(skip).limit(limit).all()
        return [ProductMapper.to_entity(m) for m in models]

    def delete(self, product_id: int) -> bool:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        search_term = f"%{query}%"
        models = self.db.query(ProductModel).filter(
            or_(
                ProductModel.name.ilike(search_term),
                ProductModel.description.ilike(search_term),
                ProductModel.sku.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()
        return [ProductMapper.to_entity(m) for m in models]