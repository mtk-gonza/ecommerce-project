from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.interfaces.api.v1.schemas.order_schema import OrderCreateSchema, OrderSchema
from app.application.services.order_service import OrderService
from app.interfaces.api.v1.dependencies.services import get_order_service, get_cart_service
from app.interfaces.api.v1.dependencies.auth import get_current_user, get_current_admin_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, BusinessRuleException

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreateSchema, order_service: OrderService = Depends(get_order_service), cart_service = Depends(get_cart_service), current_user: User = Depends(get_current_user)):
    try:
        cart = cart_service.get_or_create_cart(user_id=current_user.id)
        order = order_service.create_order(
            user_id=current_user.id,
            cart=cart,
            shipping_address=order_data.shipping_address,
            billing_address=order_data.billing_address
        )
        cart_service.clear_cart(cart)
        return order
    except (EntityNotFoundException, BusinessRuleException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[OrderSchema])
def list_user_orders(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), order_service: OrderService = Depends(get_order_service), current_user: User = Depends(get_current_user)):
    return order_service.list_user_orders(user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, order_service: OrderService = Depends(get_order_service), current_user: User = Depends(get_current_user)):
    try:
        order = order_service.get_order(order_id)
        if order.user_id != current_user.id and not current_user.is_admin():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        return order
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{order_id}/confirm", response_model=OrderSchema)
def confirm_order(order_id: int, order_service: OrderService = Depends(get_order_service), current_user: User = Depends(get_current_admin_user)):
    try:
        return order_service.confirm_order(order_id)
    except (EntityNotFoundException, BusinessRuleException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{order_id}/cancel", response_model=OrderSchema)
def cancel_order(order_id: int, reason: str, order_service: OrderService = Depends(get_order_service), current_user: User = Depends(get_current_user)):
    try:
        return order_service.cancel_order(order_id, reason)
    except (EntityNotFoundException, BusinessRuleException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{order_id}/ship", response_model=OrderSchema)
def ship_order(order_id: int, tracking_number: str = None, order_service: OrderService = Depends(get_order_service), current_user: User = Depends(get_current_admin_user)):
    try:
        return order_service.ship_order(order_id, tracking_number)
    except (EntityNotFoundException, BusinessRuleException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))