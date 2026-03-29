from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.product import Product

class ProductRepositoryPort(ABC):
    """Puerto de repositorio de productos - Define el contrato"""
    
    @abstractmethod
    def save(self, product: Product) -> Product:
        """Crea o actualiza un producto"""
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Busca un producto por ID"""
        pass

    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[Product]:
        """Busca un producto por SKU"""
        pass

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Product]:
        """Busca un producto por slug"""
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
        """Lista todos los productos con paginación"""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Elimina un producto"""
        pass

    @abstractmethod
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Busca productos por término"""
        pass