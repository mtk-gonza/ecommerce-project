from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.category import Category

class CategoryRepositoryPort(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, category_id: int, with_relations: bool = False) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_slug(self, slug: str, with_relations: bool = False) -> Optional[Category]:
        pass

    @abstractmethod
    def find_all(self, parent_id: Optional[int] = None, is_active: bool = True) -> List[Category]:
        pass

    @abstractmethod
    def delete(self, category_id: int) -> bool:
        pass

    @abstractmethod
    def find_root_categories(self, is_active: bool = True) -> List[Category]:
        pass

    @abstractmethod
    def find_category_tree(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def has_products(self, category_id: int) -> bool:
        pass