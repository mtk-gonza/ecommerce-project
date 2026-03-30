from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.product import Product

class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        pass