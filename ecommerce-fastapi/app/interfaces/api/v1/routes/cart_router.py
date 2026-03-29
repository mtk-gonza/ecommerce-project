from fastapi import APIRouter, Depends, HTTPException, status
from app.application.services.cart_service import CartService
from app.interfaces.api.v1.dependencies.services import get_cart_service
from app.interfaces.api.v1.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, InsufficientStockException
from pydantic import BaseModel

class AddToCartSchema(BaseModel):
    product_id: int
    quantity: int = 1

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/")
def get_cart(cart_service: CartService = Depends(get_cart_service), current_user: User = Depends(get_current_user)):
    cart = cart_service.get_or_create_cart(user_id=current_user.id)
    return cart

@router.post("/items")
def add_to_cart(item_data: AddToCartSchema, cart_service: CartService = Depends(get_cart_service), current_user: User = Depends(get_current_user)):
    try:
        cart = cart_service.get_or_create_cart(user_id=current_user.id)
        cart = cart_service.add_to_cart(cart, item_data.product_id, item_data.quantity)
        return cart
    except (EntityNotFoundException, InsufficientStockException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/items/{product_id}")
def remove_from_cart(product_id: int, cart_service: CartService = Depends(get_cart_service), current_user: User = Depends(get_current_user)):
    cart = cart_service.get_or_create_cart(user_id=current_user.id)
    cart = cart_service.remove_from_cart(cart, product_id)
    return cart

@router.delete("/clear")
def clear_cart(cart_service: CartService = Depends(get_cart_service), current_user: User = Depends(get_current_user)):
    cart = cart_service.get_or_create_cart(user_id=current_user.id)
    cart = cart_service.clear_cart(cart)
    return cart