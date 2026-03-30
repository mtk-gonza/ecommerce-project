from fastapi import APIRouter, Depends, HTTPException, status, Query, Cookie
from typing import Optional, List, Dict, Any
from app.interfaces.api.v1.schemas.cart_schema import (
    CartItemCreateSchema,
    CartItemUpdateSchema,
    CartResponseSchema,
    CartSummarySchema,
    CartOperationResponseSchema,
    CartMergeSchema
)
from app.application.services.cart_service import CartService
from app.interfaces.api.v1.dependencies.services import get_cart_service
from app.interfaces.api.v1.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, ValidationError, InsufficientStockException, BusinessRuleException

router = APIRouter(prefix="/cart", tags=["Cart"])

# ==================== PUBLIC ENDPOINTS (Guest & Auth) ====================

@router.get("/", response_model=CartResponseSchema)
def get_cart(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Obtiene el carrito actual del usuario o invitado"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/summary", response_model=CartSummarySchema)
def get_cart_summary(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Obtiene el resumen del carrito para checkout"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        return cart_service.get_cart_summary(cart.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/items", response_model=CartResponseSchema)
def add_to_cart(
    item_data: CartItemCreateSchema,
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Agrega un producto al carrito"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        cart = cart_service.add_to_cart(cart.id, item_data.product_id, item_data.quantity)
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientStockException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/items/{product_id}", response_model=CartResponseSchema)
def update_cart_item(
    product_id: int,
    item_data: CartItemUpdateSchema,
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Actualiza la cantidad de un item en el carrito"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        cart = cart_service.update_cart_item(cart.id, product_id, item_data.quantity)
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientStockException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/items/{product_id}", response_model=CartResponseSchema)
def remove_from_cart(
    product_id: int,
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Remueve un producto del carrito"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        cart = cart_service.remove_from_cart(cart.id, product_id)
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/clear", response_model=CartResponseSchema)
def clear_cart(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Vacía completamente el carrito"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        cart = cart_service.clear_cart(cart.id)
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/validate", response_model=Dict[str, Any])
def validate_cart_for_checkout(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Valida que el carrito esté listo para checkout"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        return cart_service.validate_cart_for_checkout(cart.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# ==================== AUTH ONLY ENDPOINTS =================

@router.post("/merge", response_model=CartResponseSchema)
def merge_guest_cart(
    merge_data: CartMergeSchema,
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Fusiona el carrito de invitado al carrito del usuario (al registrarse/login)"""
    try:
        # Solo permitir merge si el user_id coincide con el usuario actual
        if merge_data.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        
        cart = cart_service.merge_guest_cart(merge_data.session_id, merge_data.user_id)
        return cart
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/stats")
def get_cart_stats(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    current_user: Optional[User] = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    """Obtiene estadísticas rápidas del carrito"""
    try:
        if current_user:
            cart = cart_service.get_or_create_cart(user_id=current_user.id)
        elif session_id:
            cart = cart_service.get_or_create_cart(session_id=session_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticación o session_id")
        
        totals = cart_service.calculate_cart_totals(cart)
        return {
            "items_count": sum(item.quantity for item in cart.items),
            "unique_items": len(cart.items),
            "subtotal": totals["subtotal"],
            "total": totals["total"],
            "free_shipping_progress": min(100, float(cart_service.calculate_cart_totals(cart)["subtotal"] / cart_service.FREE_SHIPPING_THRESHOLD * 100))
        }
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))