from app.domain.entities.product import Product, Specification, ProductImage
from app.infrastructure.db.models.product_model import ProductModel, ProductImageModel, ProductSpecificationModel
from decimal import Decimal
from typing import List

class ProductMapper:
    @staticmethod
    def to_entity(model: ProductModel) -> Product:
        specifications = [
            Specification(key=spec.key, value=spec.value)
            for spec in model.specifications
        ]
        images = [
            ProductImage(
                id=img.id,
                url=img.url,
                alt_text=img.alt_text,
                sort_order=img.sort_order,
                is_main=img.is_main
            )
            for img in model.images
        ]
        return Product(
            id=model.id,
            sku=model.sku,
            slug=model.slug,
            name=model.name,
            description=model.description,
            base_price=Decimal(str(model.base_price)),
            currency=model.currency,
            cost_price=Decimal(str(model.cost_price)) if model.cost_price else None,
            discount_price=Decimal(str(model.discount_price)) if model.discount_price else None,
            stock=model.stock,
            low_stock_threshold=model.low_stock_threshold,
            weight=Decimal(str(model.weight)) if model.weight else None,
            dimensions=model.dimensions,
            status=model.status,
            is_visible=model.is_visible,
            is_featured=model.is_featured,
            category_id=model.category_id,
            specifications=specifications,
            images=images,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Product) -> ProductModel:
        model = ProductModel(
            id=entity.id,
            sku=entity.sku,
            slug=entity.slug,
            name=entity.name,
            description=entity.description,
            base_price=float(entity.base_price),
            currency=entity.currency,
            cost_price=float(entity.cost_price) if entity.cost_price else None,
            discount_price=float(entity.discount_price) if entity.discount_price else None,
            stock=entity.stock,
            low_stock_threshold=entity.low_stock_threshold,
            weight=float(entity.weight) if entity.weight else None,
            dimensions=entity.dimensions,
            status=entity.status,
            is_visible=entity.is_visible,
            is_featured=entity.is_featured,
            category_id=entity.category_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
        return model

    @staticmethod
    def specifications_to_models(product_id: int, specifications: List[Specification]) -> List[ProductSpecificationModel]:
        return [
            ProductSpecificationModel(product_id=product_id, key=spec.key, value=spec.value)
            for spec in specifications
        ]

    @staticmethod
    def images_to_models(product_id: int, images: List[ProductImage]) -> List[ProductImageModel]:
        return [
            ProductImageModel(
                product_id=product_id,
                url=img.url,
                alt_text=img.alt_text,
                sort_order=img.sort_order,
                is_main=img.is_main
            )
            for img in images
        ]