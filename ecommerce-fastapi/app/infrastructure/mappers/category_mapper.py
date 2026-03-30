from app.domain.entities.category import Category
from app.infrastructure.db.models.category_model import CategoryModel
from typing import List, Optional

class CategoryMapper:
    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            slug=model.slug,
            description=model.description,
            image_url=model.image_url,
            parent_id=model.parent_id,
            parent=None,
            subcategories=[],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            description=entity.description,
            image_url=entity.image_url,
            parent_id=entity.parent_id,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_entity_with_relations(model: CategoryModel) -> Category:
        entity = Category(
            id=model.id,
            name=model.name,
            slug=model.slug,
            description=model.description,
            image_url=model.image_url,
            parent_id=model.parent_id,
            parent=CategoryMapper.to_entity(model.parent) if model.parent else None,
            subcategories=[CategoryMapper.to_entity(sub) for sub in model.subcategories],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        return entity