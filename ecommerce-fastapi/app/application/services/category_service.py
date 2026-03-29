from typing import List, Optional
from app.domain.entities.category import Category
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.domain.exceptions import EntityNotFoundException
from app.utils.slug_handler import generate_slug

class CategoryService:
    def __init__(self, category_repository: CategoryRepositoryPort):
        self.category_repository = category_repository

    def create_category(self, name: str, parent_id: Optional[int] = None, description: str = None) -> Category:
        slug = generate_slug(name)
        category = Category(id=None, name=name, slug=slug, parent_id=parent_id, description=description)
        return self.category_repository.save(category)

    def get_category(self, category_id: int) -> Category:
        category = self.category_repository.find_by_id(category_id)
        if not category:
            raise EntityNotFoundException(f"Categoría {category_id} no encontrada")
        return category

    def list_categories(self, parent_id: Optional[int] = None) -> List[Category]:
        return self.category_repository.find_all(parent_id=parent_id)

    def delete_category(self, category_id: int) -> bool:
        category = self.get_category(category_id)
        return self.category_repository.delete(category_id)