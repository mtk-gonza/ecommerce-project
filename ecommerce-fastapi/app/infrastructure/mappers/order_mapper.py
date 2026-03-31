from app.domain.entities.order import Order, OrderItem, OrderStatusHistory
from app.infrastructure.db.models.order_model import OrderModel, OrderItemModel, OrderStatusHistoryModel
from app.domain.enums import OrderStatus, Currency
from decimal import Decimal
from typing import List, Optional

class OrderMapper:
    """Mapper para convertir entre entidad Order y modelo SQLAlchemy"""

    @staticmethod
    def to_entity(model: OrderModel) -> Order:
        """Convierte modelo SQLAlchemy a entidad de dominio"""
        items = [
            OrderItem(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=Decimal(str(item.unit_price)),
                total_price=Decimal(str(item.total_price))
            )
            for item in model.items
        ]
        
        status_history = [
            OrderStatusHistory(
                id=h.id,
                order_id=h.order_id,
                status=h.status,
                commented_by=h.commented_by,
                comment=h.comment,
                created_at=h.created_at
            )
            for h in model.status_history
        ]
        
        return Order(
            id=model.id,
            order_number=model.order_number,
            user_id=model.user_id,
            status=model.status,
            currency=model.currency,
            shipping_address=model.shipping_address,
            billing_address=model.billing_address,
            subtotal=Decimal(str(model.subtotal)),
            tax_amount=Decimal(str(model.tax_amount)),
            shipping_cost=Decimal(str(model.shipping_cost)),
            discount_amount=Decimal(str(model.discount_amount)),
            total_amount=Decimal(str(model.total_amount)),
            items=items,
            status_history=status_history,
            notes=model.notes,
            payment_reference=model.payment_reference,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Order) -> OrderModel:
        """Convierte entidad de dominio a modelo SQLAlchemy"""
        return OrderModel(
            id=entity.id,
            order_number=entity.order_number,
            user_id=entity.user_id,
            status=entity.status,
            currency=entity.currency,
            shipping_address=entity.shipping_address,
            billing_address=entity.billing_address,
            subtotal=float(entity.subtotal),
            tax_amount=float(entity.tax_amount),
            shipping_cost=float(entity.shipping_cost),
            discount_amount=float(entity.discount_amount),
            total_amount=float(entity.total_amount),
            notes=entity.notes,
            payment_reference=entity.payment_reference,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def items_to_models(order_id: int, items: List[OrderItem]) -> List[OrderItemModel]:
        """Convierte lista de OrderItem a lista de OrderItemModel"""
        return [
            OrderItemModel(
                id=item.id,
                order_id=order_id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=float(item.unit_price),
                total_price=float(item.total_price)
            )
            for item in items
        ]

    @staticmethod
    def status_history_to_models(order_id: int, history: List[OrderStatusHistory]) -> List[OrderStatusHistoryModel]:
        """Convierte lista de OrderStatusHistory a lista de OrderStatusHistoryModel"""
        return [
            OrderStatusHistoryModel(
                id=h.id,
                order_id=order_id,
                status=h.status,
                commented_by=h.commented_by,
                comment=h.comment,
                created_at=h.created_at
            )
            for h in history
        ]