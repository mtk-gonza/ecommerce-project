from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from typing import List, Optional
from decimal import Decimal
from app.interfaces.api.v1.schemas.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductSchema,
    ProductsListResponseSchema,
    ProductStatsSchema
)
from app.application.services.product_service import ProductService
from app.interfaces.api.v1.dependencies.services import get_product_service
from app.interfaces.api.v1.dependencies.auth import get_current_user, get_current_admin_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, ValidationError, BusinessRuleException

router = APIRouter(prefix="/products", tags=["Products"])

# ==================== PUBLIC ENDPOINTS ====================

@router.get("/", response_model=ProductsListResponseSchema)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None, ge=0),
    max_price: Optional[Decimal] = Query(None, ge=0),
    is_featured: Optional[bool] = Query(None),
    search: Optional[str] = Query(None, min_length=2),
    product_service: ProductService = Depends(get_product_service)
):
    """Lista productos con filtros avanzados"""
    try:
        products = product_service.list_products(
            skip=skip,
            limit=limit,
            category_id=category_id,
            status=status,
            min_price=min_price,
            max_price=max_price,
            is_featured=is_featured,
            search=search
        )
        return {
            "success": True,
            "message": "Productos obtenidos correctamente",
            "data": products,
            "total": len(products),
            "skip": skip,
            "limit": limit
        }
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/available", response_model=ProductsListResponseSchema)
def list_available_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    product_service: ProductService = Depends(get_product_service)
):
    """Lista solo productos disponibles para compra"""
    products = product_service.list_available_products(
        skip=skip,
        limit=limit,
        category_id=category_id
    )
    return {
        "success": True,
        "message": "Productos disponibles obtenidos",
        "data": products,
        "total": len(products),
        "skip": skip,
        "limit": limit
    }

@router.get("/featured", response_model=List[ProductSchema])
def list_featured_products(
    limit: int = Query(10, ge=1, le=50),
    product_service: ProductService = Depends(get_product_service)
):
    """Lista productos destacados"""
    return product_service.list_featured_products(limit=limit)

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """Obtiene un producto por ID"""
    try:
        product = product_service.get_product(product_id)
        if not product.is_visible:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/slug/{slug}", response_model=ProductSchema)
def get_product_by_slug(
    slug: str,
    product_service: ProductService = Depends(get_product_service)
):
    """Obtiene un producto por slug (URL amigable)"""
    try:
        product = product_service.get_product_by_slug(slug)
        if not product.is_visible:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/sku/{sku}", response_model=ProductSchema)
def get_product_by_sku(
    sku: str,
    product_service: ProductService = Depends(get_product_service)
):
    """Obtiene un producto por SKU"""
    try:
        return product_service.get_product_by_sku(sku)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{product_id}/similar", response_model=List[ProductSchema])
def get_similar_products(
    product_id: int,
    limit: int = Query(5, ge=1, le=20),
    product_service: ProductService = Depends(get_product_service)
):
    """Obtiene productos similares (misma categoría)"""
    try:
        return product_service.get_similar_products(product_id, limit=limit)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# ==================== ADMIN ENDPOINTS ====================

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreateSchema,  # ✅ CORREGIDO: era 'product_'
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Crea un nuevo producto (Solo Admin)"""
    try:
        return product_service.create_product(product_data.model_dump())  # ✅ CORREGIDO
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{product_id}/media")
def upload_product_media(
    product_id: int,
    images: Optional[List[UploadFile]] = File(None),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Sube imágenes para un producto (Solo Admin) - Placeholder"""
    product = product_service.get_product(product_id)
    return {
        "success": True,
        "message": f"Imágenes procesadas para producto {product.name}",
        "uploaded": len(images) if images else 0
    }

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,  # ✅ CORREGIDO: era 'product_'
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Actualiza un producto (Solo Admin)"""
    try:
        return product_service.update_product(
            product_id,
            product_data.model_dump(exclude_unset=True)  # ✅ CORREGIDO
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.patch("/{product_id}/price", response_model=ProductSchema)
def update_product_price(
    product_id: int,
    base_price: Optional[Decimal] = Query(None, ge=0),
    discount_price: Optional[Decimal] = Query(None, ge=0),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Actualiza solo el precio de un producto (Solo Admin)"""
    try:
        product = product_service.get_product(product_id)
        new_base = base_price if base_price is not None else product.base_price
        new_discount = discount_price if discount_price is not None else product.discount_price
        return product_service.update_product_price(product_id, new_base, new_discount)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{product_id}/stock", response_model=ProductSchema)
def update_product_stock(
    product_id: int,
    stock: int = Query(..., ge=0),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Actualiza el stock de un producto (Solo Admin)"""
    try:
        return product_service.update_product_stock(product_id, stock)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{product_id}/toggle-visibility", response_model=ProductSchema)
def toggle_product_visibility(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Alterna la visibilidad de un producto (Solo Admin)"""
    try:
        return product_service.toggle_product_visibility(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{product_id}/toggle-featured", response_model=ProductSchema)
def toggle_featured_status(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Alterna el estado destacado de un producto (Solo Admin)"""
    try:
        return product_service.toggle_featured_status(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{product_id}/archive", response_model=ProductSchema)
def archive_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Archiva un producto (soft delete) (Solo Admin)"""
    try:
        return product_service.soft_delete_product(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{product_id}/restore", response_model=ProductSchema)
def restore_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Restaura un producto archivado (Solo Admin)"""
    try:
        return product_service.restore_product(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Elimina permanentemente un producto (Solo Admin)"""
    try:
        product_service.delete_product(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# ==================== REPORTS ====================

@router.get("/admin/inventory/summary", response_model=ProductStatsSchema)
def get_inventory_summary(
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Obtiene resumen del inventario (Solo Admin)"""
    return product_service.get_inventory_summary()

@router.get("/admin/low-stock", response_model=List[ProductSchema])
def get_low_stock_products(
    threshold: int = Query(10, ge=1),
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Lista productos con stock bajo (Solo Admin)"""
    all_products = product_service.list_products(limit=1000)
    return [p for p in all_products if p.stock <= threshold]

@router.get("/admin/out-of-stock", response_model=List[ProductSchema])
def get_out_of_stock_products(
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_admin_user)
):
    """Lista productos agotados (Solo Admin)"""
    all_products = product_service.list_products(limit=1000)
    return [p for p in all_products if p.is_out_of_stock()]