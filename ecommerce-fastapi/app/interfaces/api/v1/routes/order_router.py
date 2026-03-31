from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from typing import Optional, List
from decimal import Decimal
from app.interfaces.api.v1.schemas.order_schema import (
    OrderCreateFromCartSchema,
    OrderCreateDirectSchema,
    OrderSchema,
    OrderSummarySchema,
    OrdersListResponseSchema,
    OrderStatusUpdateSchema,
    OrderCancelSchema,
    OrderShipSchema,
    OrderRefundSchema,
    OrderResponseSchema,
    OrderStatsSchema
)
from app.application.services.order_service import OrderService
from app.interfaces.api.v1.dependencies.services import get_order_service
from app.interfaces.api.v1.dependencies.auth import get_current_user, get_current_admin_user
from app.domain.entities.user import User
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    InsufficientStockException,
    OrderAlreadyShippedException
)

router = APIRouter(prefix="/orders", tags=["Orders"])

# ==================== PUBLIC ENDPOINTS (User's own orders) ====================

@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    order_data: OrderCreateFromCartSchema,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Crea una orden desde el carrito del usuario"""
    try:
        order = order_service.create_order_from_cart(
            user_id=current_user.id,
            cart_id=order_data.cart_id,
            shipping_address=order_data.shipping_address,
            billing_address=order_data.billing_address,
            notes=order_data.notes
        )
        return order
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientStockException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/direct", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_order_direct_debug(
    request: Request,  # ← Agregar para leer body crudo
    order_data: OrderCreateDirectSchema,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    # 🔍 DEBUG: Leer body crudo antes de que Pydantic lo parsee
    raw_body = await request.body()
    print(f"🔍 [DEBUG] Raw body bytes: {raw_body}")
    print(f"🔍 [DEBUG] Raw body decoded: {raw_body.decode('utf-8')}")
    
    # Tu lógica original:
    items = [item.model_dump() for item in order_data.items]
    order = order_service.create_order_direct(
        user_id=current_user.id,
        items=items,
        shipping_address=order_data.shipping_address,
        billing_address=order_data.billing_address,
        notes=order_data.notes
    )
    return order

@router.get("/", response_model=OrdersListResponseSchema)
def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene las órdenes del usuario actual"""
    from app.domain.enums import OrderStatus
    status_enum = OrderStatus(status_filter) if status_filter else None
    
    orders = order_service.get_user_orders(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status_enum
    )
    
    summaries = [
        OrderSummarySchema(
            id=o.id,
            order_number=o.order_number,
            status=o.status.value,
            total_amount=o.total_amount,
            total_items=o.total_items,
            created_at=o.created_at
        )
        for o in orders
    ]
    
    return {
        "success": True,
        "message": "Órdenes obtenidas",
        "orders": summaries,
        "total": len(orders),
        "skip": skip,
        "limit": limit
    }

@router.get("/{order_id}", response_model=OrderSchema)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene una orden específica del usuario"""
    try:
        order = order_service.get_order(order_id, user_id=current_user.id)
        return order
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.get("/number/{order_number}", response_model=OrderSchema)
def get_order_by_number(
    order_number: str,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene una orden por su número"""
    try:
        order = order_service.get_order_by_number(order_number, user_id=current_user.id)
        return order
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.post("/{order_id}/cancel", response_model=OrderSchema)
def cancel_order(
    order_id: int,
    cancel_data: OrderCancelSchema,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Cancela una orden del usuario"""
    try:
        order = order_service.cancel_order(
            order_id,
            reason=cancel_data.reason,
            commented_by=current_user.id
        )
        return order
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OrderAlreadyShippedException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{order_id}/validate-payment")
def validate_order_for_payment(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Valida que una orden esté lista para pago"""
    try:
        result = order_service.validate_order_for_payment(order_id)
        return result
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# ==================== ADMIN ENDPOINTS ====================

@router.get("/admin/", response_model=OrdersListResponseSchema)
def get_admin_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene órdenes con filtros avanzados (Solo Admin)"""
    from app.domain.enums import OrderStatus
    status_enum = OrderStatus(status_filter) if status_filter else None
    
    orders = order_service.get_admin_orders(
        skip=skip,
        limit=limit,
        user_id=user_id,
        status=status_enum,
        date_from=date_from,
        date_to=date_to
    )
    
    summaries = [
        OrderSummarySchema(
            id=o.id,
            order_number=o.order_number,
            status=o.status.value,
            total_amount=o.total_amount,
            total_items=o.total_items,
            created_at=o.created_at
        )
        for o in orders
    ]
    
    return {
        "success": True,
        "message": "Órdenes obtenidas",
        "orders": summaries,
        "total": len(orders),
        "skip": skip,
        "limit": limit
    }

@router.get("/admin/pending", response_model=List[OrderSchema])
def get_pending_orders(
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene órdenes pendientes de procesamiento (Solo Admin)"""
    return order_service.get_pending_orders(limit=limit)

@router.post("/admin/{order_id}/confirm", response_model=OrderSchema)
def admin_confirm_order(
    order_id: int,
    comment: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Confirma una orden pendiente (Solo Admin)"""
    try:
        return order_service.confirm_order(order_id, commented_by=current_user.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/admin/{order_id}/process", response_model=OrderSchema)
def admin_start_processing(
    order_id: int,
    comment: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Inicia procesamiento de orden confirmada (Solo Admin)"""
    try:
        return order_service.start_processing(order_id, commented_by=current_user.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/admin/{order_id}/ship", response_model=OrderSchema)
def admin_ship_order(
    order_id: int,
    ship_data: OrderShipSchema,
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Marca orden como enviada con tracking (Solo Admin)"""
    try:
        return order_service.ship_order(
            order_id,
            tracking_number=ship_data.tracking_number,
            commented_by=current_user.id
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/admin/{order_id}/deliver", response_model=OrderSchema)
def admin_deliver_order(
    order_id: int,
    comment: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Marca orden como entregada (Solo Admin)"""
    try:
        return order_service.deliver_order(order_id, commented_by=current_user.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/admin/{order_id}/refund", response_model=OrderSchema)
def admin_refund_order(
    order_id: int,
    refund_data: OrderRefundSchema,
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Procesa reembolso de orden (Solo Admin)"""
    try:
        return order_service.refund_order(
            order_id,
            amount=refund_data.amount,
            commented_by=current_user.id
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/admin/stats", response_model=OrderStatsSchema)
def get_order_stats(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene estadísticas de órdenes (Solo Admin)"""
    return order_service.get_order_stats(date_from=date_from, date_to=date_to)

@router.get("/admin/revenue", response_model=dict)
def get_revenue_report(
    date_from: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    date_to: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends(get_order_service)
):
    """Reporte de ingresos por período (Solo Admin)"""
    return order_service.get_revenue_report(date_from=date_from, date_to=date_to)