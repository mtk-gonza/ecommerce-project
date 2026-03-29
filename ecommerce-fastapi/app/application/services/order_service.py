from typing import List, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
import uuid
from datetime import datetime
from app.domain.entities.order import Order, OrderItem
from app.domain.entities.cart import Cart
from app.domain.enums import OrderStatus, Currency
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.exceptions import EntityNotFoundException, BusinessRuleException, InsufficientStockException

class OrderService:
    def __init__(self, order_repository: OrderRepositoryPort, product_repository: ProductRepositoryPort):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def create_order(self, user_id: int, cart: Cart, shipping_address: str, billing_address: str, tax_rate: Decimal = Decimal("0.16"), shipping_cost: Decimal = Decimal("0")) -> Order:
        if cart.is_empty():
            raise BusinessRuleException("No se puede crear una orden con carrito vacío")
        
        # Verificar stock y reducir
        for item in cart.items:
            product = self.product_repository.find_by_id(item.product_id)
            if not product:
                raise EntityNotFoundException(f"Producto {item.product_id} no encontrado")
            product.reduce_stock(item.quantity)
            self.product_repository.save(product)
        
        # Crear items de orden
        order_items = [
            OrderItem(
                id=None,
                product_id=item.product_id,
                product_name=item.product_name,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            for item in cart.items
        ]
        
        # Calcular totales
        subtotal = cart.subtotal
        tax_amount = subtotal * tax_rate
        
        order = Order(
            id=None,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=user_id,
            status=OrderStatus.PENDING,
            currency=Currency.USD,
            shipping_address=shipping_address,
            billing_address=billing_address,
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            discount_amount=Decimal("0"),
            items=order_items
        )
        
        return self.order_repository.save(order)

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Orden {order_id} no encontrada")
        return order

    def get_order_by_number(self, order_number: str) -> Order:
        order = self.order_repository.find_by_order_number(order_number)
        if not order:
            raise EntityNotFoundException(f"Orden {order_number} no encontrada")
        return order

    def list_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        return self.order_repository.find_by_user_id(user_id=user_id, skip=skip, limit=limit)

    def confirm_order(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        order.confirm()
        return self.order_repository.save(order)

    def cancel_order(self, order_id: int, reason: str) -> Order:
        order = self.get_order(order_id)
        order.cancel(reason)
        # Restaurar stock
        for item in order.items:
            product = self.product_repository.find_by_id(item.product_id)
            if product:
                product.increase_stock(item.quantity)
                self.product_repository.save(product)
        return self.order_repository.save(order)

    def ship_order(self, order_id: int, tracking_number: Optional[str] = None) -> Order:
        order = self.get_order(order_id)
        order.ship(tracking_number)
        return self.order_repository.save(order)