from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from app.domain.entities.product import Product, Specification, ProductImage
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    InsufficientStockException,
    InvalidPriceException,
    BusinessRuleException
)
from app.utils.slug_handler import generate_slug
from app.domain.enums import ProductStatus

class ProductService:
    """
    Servicio de Productos - Capa de Aplicación
    Contiene toda la lógica de negocio relacionada con productos
    """
    
    def __init__(
        self,
        product_repository: ProductRepositoryPort,
        category_repository: Optional[CategoryRepositoryPort] = None
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    # ==================== CREATE ====================
    
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """Crea un nuevo producto con validaciones completas"""
        
        # 1. Validar SKU único
        if 'sku' in product_data:
            existing = self.product_repository.find_by_sku(product_data['sku'])
            if existing:
                raise ValidationError(f"El SKU '{product_data['sku']}' ya está registrado")
        
        # 2. Validar categoría si se proporciona
        if product_data.get('category_id'):
            if self.category_repository:
                category = self.category_repository.find_by_id(product_data['category_id'])
                if not category:
                    raise EntityNotFoundException(f"Categoría {product_data['category_id']} no encontrada")
                if not category.is_active:
                    raise BusinessRuleException("No se pueden crear productos en categorías inactivas")
        
        # 3. Generar slug si no existe
        if not product_data.get('slug') and 'name' in product_data:
            base_slug = generate_slug(product_data['name'])
            slug = base_slug
            counter = 1
            # Asegurar slug único
            while self.product_repository.find_by_slug(slug):
                slug = f"{base_slug}-{counter}"
                counter += 1
            product_data['slug'] = slug
        elif product_data.get('slug'):
            # Validar slug único si se proporciona
            existing = self.product_repository.find_by_slug(product_data['slug'])
            if existing:
                raise ValidationError(f"El slug '{product_data['slug']}' ya está en uso")
        
        # 4. Validar precio de descuento
        if product_data.get('discount_price') and product_data.get('base_price'):
            if product_data['discount_price'] > product_data['base_price']:
                raise InvalidPriceException("El precio con descuento no puede ser mayor al precio base")
        
        # 5. Crear y guardar entidad
        product = Product(id=None, **{k: v for k, v in product_data.items() if k != 'id'})
        return self.product_repository.save(product)

    def create_product_with_media(
        self,
        product_data: Dict[str, Any],
        images: Optional[List[Dict[str, Any]]] = None,
        specifications: Optional[List[Dict[str, str]]] = None
    ) -> Product:
        """Crea un producto con imágenes y especificaciones"""
        product = self.create_product(product_data)
        
        # Agregar imágenes
        if images:
            for idx, img_data in enumerate(images):
                image = ProductImage(
                    id=None,
                    url=img_data['url'],
                    alt_text=img_data.get('alt_text'),
                    sort_order=img_data.get('sort_order', idx),
                    is_main=img_data.get('is_main', idx == 0)
                )
                product.images.append(image)
        
        # Agregar especificaciones
        if specifications:
            for spec_data in specifications:
                spec = Specification(key=spec_data['key'], value=spec_data['value'])
                product.specifications.append(spec)
        
        return self.product_repository.save(product)

    # ==================== READ ====================
    
    def get_product(self, product_id: int) -> Product:
        """Obtiene un producto por ID"""
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException(f"Producto con ID {product_id} no encontrado")
        return product

    def get_product_by_slug(self, slug: str) -> Product:
        """Obtiene un producto por slug (URLs amigables)"""
        product = self.product_repository.find_by_slug(slug)
        if not product:
            raise EntityNotFoundException(f"Producto con slug '{slug}' no encontrado")
        return product

    def get_product_by_sku(self, sku: str) -> Product:
        """Obtiene un producto por SKU"""
        product = self.product_repository.find_by_sku(sku)
        if not product:
            raise EntityNotFoundException(f"Producto con SKU '{sku}' no encontrado")
        return product

    def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        status: Optional[str] = None,
        is_visible: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Lista productos con filtros avanzados y paginación"""
        
        # Si hay búsqueda, usar método de búsqueda
        if search and len(search.strip()) >= 2:
            return self.product_repository.search(query=search.strip(), skip=skip, limit=limit)
        
        return self.product_repository.find_all(
            skip=skip,
            limit=limit,
            category_id=category_id,
            status=status,
            is_visible=is_visible,
            is_featured=is_featured,
            min_price=min_price,
            max_price=max_price
        )

    def list_available_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None
    ) -> List[Product]:
        """Lista solo productos disponibles para compra"""
        products = self.list_products(
            skip=skip,
            limit=limit,
            category_id=category_id,
            is_visible=True
        )
        return [p for p in products if p.is_available]

    def list_featured_products(self, limit: int = 10) -> List[Product]:
        """Lista productos destacados"""
        return self.product_repository.find_featured(limit=limit)

    def get_products_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos de una categoría específica"""
        if self.category_repository:
            category = self.category_repository.find_by_id(category_id)
            if not category:
                raise EntityNotFoundException(f"Categoría {category_id} no encontrada")
            if not category.is_active:
                raise BusinessRuleException("La categoría está inactiva")
        
        return self.list_products(skip=skip, limit=limit, category_id=category_id)

    def get_similar_products(self, product_id: int, limit: int = 5) -> List[Product]:
        """Obtiene productos similares (misma categoría)"""
        product = self.get_product(product_id)
        if not product.category_id:
            return []
        
        products = self.list_products(category_id=product.category_id, limit=limit + 1)
        similar = [p for p in products if p.id != product_id]
        return similar[:limit]

    # ==================== UPDATE ====================
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Product:
        """Actualiza un producto existente"""
        product = self.get_product(product_id)
        
        # Campos protegidos (no se pueden actualizar)
        protected_fields = ['id', 'created_at', 'sku', 'slug']
        
        # Validar SKU si se intenta cambiar
        if 'sku' in product_data and product_data['sku'] != product.sku:
            existing = self.product_repository.find_by_sku(product_data['sku'])
            if existing and existing.id != product_id:
                raise ValidationError(f"El SKU '{product_data['sku']}' ya está registrado")
        
        # Validar slug si se intenta cambiar
        if 'slug' in product_data and product_data['slug'] != product.slug:
            existing = self.product_repository.find_by_slug(product_data['slug'])
            if existing and existing.id != product_id:
                raise ValidationError(f"El slug '{product_data['slug']}' ya está en uso")
        
        # Validar precio de descuento
        base_price = product_data.get('base_price', product.base_price)
        discount_price = product_data.get('discount_price', product.discount_price)
        if discount_price is not None and discount_price > base_price:
            raise InvalidPriceException("El precio con descuento no puede ser mayor al precio base")
        
        # Actualizar campos permitidos
        for key, value in product_data.items():
            if key not in protected_fields and hasattr(product, key) and value is not None:
                setattr(product, key, value)
        
        product._validate()
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def update_product_price(self, product_id: int, base_price: Decimal, discount_price: Optional[Decimal] = None) -> Product:
        """Actualiza solo el precio de un producto"""
        product = self.get_product(product_id)
        
        if base_price < 0:
            raise InvalidPriceException("El precio base no puede ser negativo")
        if discount_price is not None and discount_price < 0:
            raise InvalidPriceException("El precio con descuento no puede ser negativo")
        if discount_price is not None and discount_price > base_price:
            raise InvalidPriceException("El precio con descuento no puede ser mayor al precio base")
        
        product.base_price = base_price
        product.discount_price = discount_price
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def update_product_stock(self, product_id: int, stock: int) -> Product:
        """Actualiza el stock de un producto"""
        product = self.get_product(product_id)
        if stock < 0:
            raise ValidationError("El stock no puede ser negativo")
        
        product.stock = stock
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def update_product_status(self, product_id: int, status: str) -> Product:
        """Actualiza el estado de un producto"""
        from app.domain.enums import ProductStatus
        
        product = self.get_product(product_id)
        try:
            product_status = ProductStatus(status)
        except ValueError:
            valid_statuses = [s.value for s in ProductStatus]
            raise ValidationError(f"Estado inválido. Permitidos: {valid_statuses}")
        
        product.status = product_status
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def toggle_product_visibility(self, product_id: int) -> Product:
        """Alterna la visibilidad de un producto"""
        product = self.get_product(product_id)
        product.is_visible = not product.is_visible
        product.updated_at = datetime.now()
        return self.product_repository.save(product)

    def toggle_featured_status(self, product_id: int) -> Product:
        """Alterna el estado destacado de un producto"""
        product = self.get_product(product_id)
        product.is_featured = not product.is_featured
        product.updated_at = datetime.now()
        return self.product_repository.save(product)

    # ==================== STOCK MANAGEMENT ====================
    
    def reduce_stock(self, product_id: int, quantity: int) -> Product:
        """Reduce el stock (usado al crear órdenes)"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        product = self.get_product(product_id)
        product.reduce_stock(quantity)
        return self.product_repository.save(product)

    def increase_stock(self, product_id: int, quantity: int) -> Product:
        """Aumenta el stock (usado al cancelar órdenes o recibir inventario)"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        product = self.get_product(product_id)
        product.increase_stock(quantity)
        return self.product_repository.save(product)

    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """Verifica si hay stock suficiente"""
        product = self.get_product(product_id)
        return product.stock >= quantity

    def bulk_reduce_stock(self, items: List[Dict[str, int]]) -> List[Product]:
        """Reduce stock de múltiples productos"""
        updated = []
        for item in items:
            product = self.reduce_stock(item['product_id'], item['quantity'])
            updated.append(product)
        return updated

    def bulk_increase_stock(self, items: List[Dict[str, int]]) -> List[Product]:
        """Aumenta stock de múltiples productos"""
        updated = []
        for item in items:
            product = self.increase_stock(item['product_id'], item['quantity'])
            updated.append(product)
        return updated

    # ==================== DELETE ====================
    
    def delete_product(self, product_id: int) -> bool:
        """Elimina físicamente un producto"""
        product = self.get_product(product_id)
        # Verificar si tiene órdenes asociadas (opcional, depende de tu repo)
        return self.product_repository.delete(product_id)

    def soft_delete_product(self, product_id: int) -> Product:
        """Elimina lógicamente un producto (cambia estado a ARCHIVED)"""
        from app.domain.enums import ProductStatus
        product = self.get_product(product_id)
        product.status = ProductStatus.ARCHIVED
        product.is_visible = False
        product.updated_at = datetime.now()
        return self.product_repository.save(product)

    def restore_product(self, product_id: int) -> Product:
        """Restaura un producto archivado"""
        from app.domain.enums import ProductStatus
        product = self.get_product(product_id)
        if product.status != ProductStatus.ARCHIVED:
            raise BusinessRuleException("Solo se pueden restaurar productos archivados")
        product.status = ProductStatus.ACTIVE
        product.is_visible = True
        product.updated_at = datetime.now()
        return self.product_repository.save(product)

    # ==================== UTILS & REPORTS ====================
    
    def get_product_with_related(self, product_id: int) -> Dict[str, Any]:
        """Obtiene producto con toda su información relacionada"""
        product = self.get_product(product_id)
        return {
            'product': product,
            'specifications': product.specifications,
            'images': product.images,
            'category': product.category,
            'final_price': product.final_price,
            'has_discount': product.has_discount,
            'discount_percentage': product.discount_percentage,
            'is_available': product.is_available,
            'is_low_stock': product.is_low_stock(),
            'is_out_of_stock': product.is_out_of_stock()
        }

    def calculate_inventory_value(self) -> Decimal:
        """Calcula el valor total del inventario"""
        all_products = self.product_repository.find_all(limit=10000)
        total = Decimal("0")
        for p in all_products:
            cost = p.cost_price if p.cost_price else p.base_price
            total += cost * p.stock
        return total

    def get_inventory_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del inventario"""
        all_products = self.product_repository.find_all(limit=10000)
        
        return {
            'total_products': len(all_products),
            'active_products': len([p for p in all_products if p.status.value == 'active']),
            # ✅ CORREGIDO: Solo contar low stock en productos activos
            'low_stock_products': len([
                p for p in all_products 
                if p.status == ProductStatus.ACTIVE and p.is_low_stock()
            ]),
            'out_of_stock_products': len([
                p for p in all_products 
                if p.is_out_of_stock() and p.status.value == 'active'
            ]),
            'featured_products': len([p for p in all_products if p.is_featured]),
            'inventory_value': self.calculate_inventory_value()
        }

    def search_products(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Búsqueda full-text en productos"""
        if not query or len(query.strip()) < 2:
            raise ValidationError("El término de búsqueda debe tener al menos 2 caracteres")
        return self.product_repository.search(query=query.strip(), skip=skip, limit=limit)