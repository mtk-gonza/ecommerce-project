from typing import List, Optional
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

class ProductService:
    def __init__(self, product_repository: ProductRepositoryPort, category_repository: Optional[CategoryRepositoryPort] = None):
        self.product_repository = product_repository
        self.category_repository = category_repository

    # ==================== CREATE ====================
    
    def create_product(self, product_data: dict) -> Product:
        if 'sku' in product_data:
            existing = self.product_repository.find_by_sku(product_data['sku'])
            if existing:
                raise ValidationError(f"El SKU '{product_data['sku']}' ya está registrado")
        if product_data.get('category_id'):
            category = self.category_repository.find_by_id(product_data['category_id']) if self.category_repository else None
            if not category:
                raise EntityNotFoundException(f"Categoría {product_data['category_id']} no encontrada")
        if not product_data.get('slug') and 'name' in product_data:
            product_data['slug'] = generate_slug(product_data['name'])
        else:
            existing = self.product_repository.find_by_slug(product_data['slug'])
            if existing:
                raise ValidationError(f"El slug '{product_data['slug']}' ya está en uso")
        if product_data.get('discount_price') and product_data.get('base_price'):
            if product_data['discount_price'] > product_data['base_price']:
                raise InvalidPriceException("El precio con descuento no puede ser mayor al precio base")
        product = Product(**product_data)
        return self.product_repository.save(product)

    def create_product_with_images(self, product_data: dict, images: List[dict]) -> Product:
        product = self.create_product(product_data)
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
            product = self.product_repository.save(product)    
        return product

    def create_product_with_specifications(self, product_data: dict, specifications: List[dict]) -> Product:
        product = self.create_product(product_data)
        if specifications:
            for spec_data in specifications:
                specification = Specification(
                    key=spec_data['key'],
                    value=spec_data['value']
                )
                product.specifications.append(specification)
            
            product = self.product_repository.save(product)
        return product


    # ==================== READ ====================
    
    def get_product(self, product_id: int) -> Product:
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException(f"Producto con ID {product_id} no encontrado")
        return product

    def get_product_by_slug(self, slug: str) -> Product:
        product = self.product_repository.find_by_slug(slug)
        if not product:
            raise EntityNotFoundException(f"Producto con slug '{slug}' no encontrado")
        return product

    def get_product_by_sku(self, sku: str) -> Product:
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
        max_price: Optional[Decimal] = None
    ) -> List[Product]:
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

    def list_available_products(self, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
        products = self.list_products(
            skip=skip,
            limit=limit,
            category_id=category_id,
            is_visible=True
        )
        return [p for p in products if p.is_available]

    def list_featured_products(self, limit: int = 10) -> List[Product]:
        return self.product_repository.find_featured(limit=limit)

    def search_products(self, query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        if not query or len(query.strip()) < 2:
            raise ValidationError("El término de búsqueda debe tener al menos 2 caracteres")
        
        return self.product_repository.search(query=query.strip(), skip=skip, limit=limit)

    def get_low_stock_products(self, threshold: Optional[int] = None) -> List[Product]:
        if threshold is None:
            threshold = 10
        all_products = self.product_repository.find_all(limit=1000)
        return [p for p in all_products if p.stock <= threshold]

    def get_out_of_stock_products(self) -> List[Product]:
        all_products = self.product_repository.find_all(limit=1000)
        return [p for p in all_products if p.is_out_of_stock()]


    # ==================== UPDATE ====================
    
    def update_product(self, product_id: int, product_data: dict) -> Product:
        product = self.get_product(product_id)
        protected_fields = ['id', 'created_at', 'sku']
        if 'sku' in product_data and product_data['sku'] != product.sku:
            existing = self.product_repository.find_by_sku(product_data['sku'])
            if existing and existing.id != product_id:
                raise ValidationError(f"El SKU '{product_data['sku']}' ya está registrado")
        if 'slug' in product_data and product_data['slug'] != product.slug:
            existing = self.product_repository.find_by_slug(product_data['slug'])
            if existing and existing.id != product_id:
                raise ValidationError(f"El slug '{product_data['slug']}' ya está en uso")
        for key, value in product_data.items():
            if key not in protected_fields and hasattr(product, key):
                setattr(product, key, value)
        product._validate()
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def update_product_price(self, product_id: int, base_price: Decimal, discount_price: Optional[Decimal] = None) -> Product:
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
        product = self.get_product(product_id)
        
        if stock < 0:
            raise ValidationError("El stock no puede ser negativo")
        
        product.stock = stock
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def update_product_status(self, product_id: int, status: str) -> Product:
        from app.domain.enums import ProductStatus
        
        product = self.get_product(product_id)
        
        try:
            product_status = ProductStatus(status)
        except ValueError:
            raise ValidationError(f"Estado inválido. Estados permitidos: {[s.value for s in ProductStatus]}")
        
        product.status = product_status
        product.updated_at = datetime.now()
        
        return self.product_repository.save(product)

    def activate_product(self, product_id: int) -> Product:
        from app.domain.enums import ProductStatus
        return self.update_product_status(product_id, ProductStatus.ACTIVE.value)

    def deactivate_product(self, product_id: int) -> Product:
        from app.domain.enums import ProductStatus
        return self.update_product_status(product_id, ProductStatus.INACTIVE.value)

    def toggle_product_visibility(self, product_id: int) -> Product:
        product = self.get_product(product_id)
        product.is_visible = not product.is_visible
        product.updated_at = datetime.now()
        return self.product_repository.save(product)

    def toggle_featured_status(self, product_id: int) -> Product:
        product = self.get_product(product_id)
        product.is_featured = not product.is_featured
        product.updated_at = datetime.now()
        return self.product_repository.save(product)
    

    # ==================== STOCK MANAGEMENT ====================
    
    def reduce_stock(self, product_id: int, quantity: int) -> Product:
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        product = self.get_product(product_id)
        product.reduce_stock(quantity)
        
        return self.product_repository.save(product)

    def increase_stock(self, product_id: int, quantity: int) -> Product:
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        product = self.get_product(product_id)
        product.increase_stock(quantity)
        
        return self.product_repository.save(product)

    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        product = self.get_product(product_id)
        return product.stock >= quantity

    def bulk_reduce_stock(self, items: List[dict]) -> List[Product]:
        updated_products = []
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            product = self.reduce_stock(product_id, quantity)
            updated_products.append(product)
        
        return updated_products

    def bulk_increase_stock(self, items: List[dict]) -> List[Product]:
        updated_products = []
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            product = self.increase_stock(product_id, quantity)
            updated_products.append(product)
        
        return updated_products


    # ==================== DELETE ====================
    
    def delete_product(self, product_id: int) -> bool:
        product = self.get_product(product_id)
        # Verificar si el producto tiene órdenes asociadas
        # Esto dependería de si tu repositorio tiene este método
        # if self.product_repository.has_orders(product_id):
        #     raise BusinessRuleException("No se puede eliminar un producto con órdenes asociadas")
        return self.product_repository.delete(product_id)

    def soft_delete_product(self, product_id: int) -> Product:
        from app.domain.enums import ProductStatus
        product = self.get_product(product_id)
        product.status = ProductStatus.ARCHIVED
        product.is_visible = False
        product.updated_at = datetime.now()
        return self.product_repository.save(product)


    # ==================== UTILS ====================
    
    def get_product_with_related(self, product_id: int) -> dict:
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

    def get_products_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        if self.category_repository:
            category = self.category_repository.find_by_id(category_id)
            if not category:
                raise EntityNotFoundException(f"Categoría {category_id} no encontrada")
        
        return self.list_products(skip=skip, limit=limit, category_id=category_id)

    def get_similar_products(self, product_id: int, limit: int = 5) -> List[Product]:
        product = self.get_product(product_id)
        
        if not product.category_id:
            return []
        
        products = self.list_products(
            category_id=product.category_id,
            limit=limit + 1
        )
        
        similar = [p for p in products if p.id != product_id]
        
        return similar[:limit]

    def calculate_inventory_value(self) -> Decimal:
        all_products = self.product_repository.find_all(limit=1000)
        total_value = Decimal("0")
        
        for product in all_products:
            if product.cost_price:
                total_value += product.cost_price * product.stock
            else:
                total_value += product.base_price * product.stock
        
        return total_value

    def get_inventory_summary(self) -> dict:
        all_products = self.product_repository.find_all(limit=1000)
        
        total_products = len(all_products)
        active_products = len([p for p in all_products if p.status.value == 'active'])
        low_stock_products = len([p for p in all_products if p.is_low_stock()])
        out_of_stock_products = len([p for p in all_products if p.is_out_of_stock()])
        featured_products = len([p for p in all_products if p.is_featured])
        
        return {
            'total_products': total_products,
            'active_products': active_products,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'featured_products': featured_products,
            'inventory_value': self.calculate_inventory_value()
        }