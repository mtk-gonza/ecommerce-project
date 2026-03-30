# infrastructure/repositories/category_repository_impl.py

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.entities.category import Category
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.infrastructure.db.models.category_model import CategoryModel
from app.infrastructure.mappers.category_mapper import CategoryMapper

class CategoryRepositoryImpl(CategoryRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, category: Category) -> Category:
        model = CategoryMapper.to_model(category)
        if category.id:
            self.db.merge(model)
        else:
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return CategoryMapper.to_entity(model)

    def find_by_id(self, category_id: int, with_relations: bool = False) -> Optional[Category]:
        query = self.db.query(CategoryModel).filter(CategoryModel.id == category_id)        
        if with_relations:
            query = query.options(
                joinedload(CategoryModel.parent),
                joinedload(CategoryModel.subcategories)
            )        
        model = query.first()        
        if not model:
            return None        
        if with_relations:
            return CategoryMapper.to_entity_with_relations(model)
        return CategoryMapper.to_entity(model)

    def find_by_slug(self, slug: str, with_relations: bool = False) -> Optional[Category]:
        query = self.db.query(CategoryModel).filter(CategoryModel.slug == slug)
        if with_relations:
            query = query.options(
                joinedload(CategoryModel.parent),
                joinedload(CategoryModel.subcategories)
            )        
        model = query.first()        
        if not model:
            return None        
        if with_relations:
            return CategoryMapper.to_entity_with_relations(model)
        return CategoryMapper.to_entity(model)

    def find_all(self, parent_id: Optional[int] = None, is_active: bool = True) -> List[Category]:
        query = self.db.query(CategoryModel)        
        if parent_id is not None:
            query = query.filter(CategoryModel.parent_id == parent_id)
        if is_active:
            query = query.filter(CategoryModel.is_active == True)        
        models = query.all()
        return [CategoryMapper.to_entity(m) for m in models]

    def find_root_categories(self, is_active: bool = True) -> List[Category]:
        return self.find_all(parent_id=None, is_active=is_active)

    def find_category_tree(self, category_id: int) -> Optional[Category]:
        return self.find_by_id(category_id, with_relations=True)

    def delete(self, category_id: int) -> bool:
        model = self.db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def has_products(self, category_id: int) -> bool:
        from app.infrastructure.db.models.product_model import ProductModel
        count = self.db.query(ProductModel).filter(
            ProductModel.category_id == category_id
        ).count()
        return count > 0