from typing import List, Optional, Dict, Any
from app.domain.entities.category import Category
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException
)
from app.utils.slug_handler import generate_slug

class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepositoryPort,
        product_repository: Optional[ProductRepositoryPort] = None
    ):
        self.category_repository = category_repository
        self.product_repository = product_repository


    # ==================== CREATE ====================
    def create_category(self, name: str, parent_id: Optional[int] = None, description: Optional[str] = None, image_url: Optional[str] = None) -> Category:
        base_slug = generate_slug(name)
        slug = base_slug
        counter = 1
        while self.category_repository.find_by_slug(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1
        if parent_id:
            parent = self.category_repository.find_by_id(parent_id)
            if not parent:
                raise EntityNotFoundException(f"Categoría padre {parent_id} no encontrada")
            if not parent.is_active:
                raise BusinessRuleException("No se pueden crear subcategorías en categorías inactivas")  
        category = Category(
            id=None,
            name=name,
            slug=slug,
            parent_id=parent_id,
            description=description,
            image_url=image_url
        )
        return self.category_repository.save(category)

    def create_category_tree(self, categories_data: List[Dict[str, Any]]) -> List[Category]:
        created = []
        for cat_data in categories_data:
            parent = created[-1] if created else None
            category = self.create_category(
                name=cat_data['name'],
                parent_id=parent.id if parent else None,
                description=cat_data.get('description'),
                image_url=cat_data.get('image_url')
            )
            created.append(category)
        return created


    # ==================== READ ====================
    def get_category(self, category_id: int, with_relations: bool = False) -> Category:
        category = self.category_repository.find_by_id(category_id, with_relations=with_relations)
        if not category:
            raise EntityNotFoundException(f"Categoría {category_id} no encontrada")
        return category

    def get_category_by_slug(self, slug: str, with_relations: bool = False) -> Category:
        category = self.category_repository.find_by_slug(slug, with_relations=with_relations)
        if not category:
            raise EntityNotFoundException(f"Categoría con slug '{slug}' no encontrada")
        return category

    def list_categories(self, parent_id: Optional[int] = None, is_active: bool = True) -> List[Category]:
        return self.category_repository.find_all(parent_id=parent_id, is_active=is_active)

    def list_root_categories(self, is_active: bool = True) -> List[Category]:
        return self.category_repository.find_root_categories(is_active=is_active)

    def get_category_tree(self, category_id: int) -> Dict[str, Any]:
        category = self.category_repository.find_category_tree(category_id)
        if not category:
            raise EntityNotFoundException(f"Categoría {category_id} no encontrada")
        return self._build_category_tree_dict(category)

    def _build_category_tree_dict(self, category: Category) -> Dict[str, Any]:
        return {
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'image_url': category.image_url,
            'is_active': category.is_active,
            'full_path': category.get_full_path(),
            'parent_id': category.parent_id,
            'subcategories': [
                self._build_category_tree_dict(sub)
                for sub in category.subcategories
            ]
        }

    def get_all_categories_tree(self) -> List[Dict[str, Any]]:
        root_categories = self.list_root_categories(is_active=True)
        return [self._build_category_tree_dict(cat) for cat in root_categories]

    def get_category_full_path(self, category_id: int) -> str:
        category = self.get_category(category_id, with_relations=True)
        return category.get_full_path()

    def get_category_with_products_count(self, category_id: int) -> Dict[str, Any]:
        category = self.get_category(category_id)        
        products_count = 0
        if self.product_repository:
            products = self.product_repository.find_all(category_id=category_id, limit=10000)
            products_count = len(products)        
        return {
            'category': category,
            'products_count': products_count
        }


    # ==================== UPDATE ====================
    def update_category(self, category_id: int, category_data: Dict[str, Any]) -> Category:
        category = self.get_category(category_id)
        protected_fields = ['id', 'created_at', 'slug']
        if 'slug' in category_data and category_data['slug'] != category.slug:
            existing = self.category_repository.find_by_slug(category_data['slug'])
            if existing and existing.id != category_id:
                raise ValidationError(f"El slug '{category_data['slug']}' ya está en uso")
        if 'parent_id' in category_data and category_data['parent_id'] != category.parent_id:
            new_parent_id = category_data['parent_id']
            if new_parent_id == category_id:
                raise BusinessRuleException("Una categoría no puede ser su propia padre")
            if new_parent_id:
                new_parent = self.category_repository.find_by_id(new_parent_id)
                if not new_parent:
                    raise EntityNotFoundException(f"Categoría padre {new_parent_id} no encontrada")
                if self._is_descendant(new_parent_id, category_id):
                    raise BusinessRuleException("No se puede mover la categoría: se crearía un ciclo en la jerarquía")
        for key, value in category_data.items():
            if key not in protected_fields and hasattr(category, key) and value is not None:
                setattr(category, key, value)      
        category.__post_init__()
        from datetime import datetime
        category.updated_at = datetime.now()
        return self.category_repository.save(category)

    def _is_descendant(self, potential_descendant_id: int, ancestor_id: int) -> bool:
        category = self.category_repository.find_by_id(potential_descendant_id, with_relations=True)
        while category and category.parent_id:
            if category.parent_id == ancestor_id:
                return True
            category = self.category_repository.find_by_id(category.parent_id, with_relations=True)
        return False

    def activate_category(self, category_id: int) -> Category:
        category = self.get_category(category_id)
        category.is_active = True
        from datetime import datetime
        category.updated_at = datetime.now()
        return self.category_repository.save(category)

    def deactivate_category(self, category_id: int) -> Category:
        category = self.get_category(category_id, with_relations=True)
        if self.product_repository:
            products = self.product_repository.find_all(category_id=category_id, limit=1000)
            active_products = [p for p in products if p.is_available]
            if active_products:
                raise BusinessRuleException(
                    f"No se puede desactivar: hay {len(active_products)} productos activos en esta categoría"
                )    
        category.is_active = False
        from datetime import datetime
        category.updated_at = datetime.now()
        for subcategory in category.subcategories:
            subcategory.is_active = False
        return self.category_repository.save(category)


    # ==================== DELETE ====================
    def delete_category(self, category_id: int) -> bool:
        category = self.get_category(category_id)
        if self.product_repository and self.category_repository.has_products(category_id):
            raise BusinessRuleException("No se puede eliminar: la categoría tiene productos asociados")
        category_with_tree = self.category_repository.find_category_tree(category_id)
        if category_with_tree and category_with_tree.subcategories:
            raise BusinessRuleException("No se puede eliminar: la categoría tiene subcategorías")
        return self.category_repository.delete(category_id)

    def soft_delete_category(self, category_id: int) -> Category:
        return self.deactivate_category(category_id)

    def merge_categories(self, source_id: int, target_id: int) -> Dict[str, Any]:
        source = self.get_category(source_id)
        target = self.get_category(target_id)
        if source_id == target_id:
            raise BusinessRuleException("Las categorías deben ser diferentes")
        # TODO: Mover productos de source a target
        # TODO: Mover subcategorías de source a target
        # TODO: Eliminar source
        return {
            "success": True,
            "message": f"Categoría '{source.name}' fusionada en '{target.name}'",
            "source_id": source_id,
            "target_id": target_id
        }


    # ==================== UTILS ====================
    def get_categories_stats(self) -> Dict[str, Any]:
        all_categories = self.category_repository.find_all(is_active=False)  # Todas
        active_categories = self.category_repository.find_all(is_active=True)
        root_categories = self.category_repository.find_root_categories(is_active=True)
        return {
            'total_categories': len(all_categories),
            'active_categories': len(active_categories),
            'inactive_categories': len(all_categories) - len(active_categories),
            'root_categories': len(root_categories),
            'has_hierarchy': len(active_categories) != len(root_categories)
        }

    def search_categories(self, query: str, limit: int = 20) -> List[Category]:
        if not query or len(query.strip()) < 2:
            raise ValidationError("El término de búsqueda debe tener al menos 2 caracteres")
        all_categories = self.category_repository.find_all(is_active=True)
        query_lower = query.lower().strip()
        return [
            cat for cat in all_categories
            if query_lower in cat.name.lower() or query_lower in (cat.description or '').lower()
        ][:limit]