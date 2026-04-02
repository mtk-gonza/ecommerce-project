import uuid
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from app.domain.entities.order import Order, OrderItem
from app.domain.entities.cart import Cart
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.ports.cart_repository import CartRepositoryPort
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    InsufficientStockException,
    OrderAlreadyShippedException
)
from app.domain.enums import OrderStatus
from app.infrastructure.logging import get_logger, log_with_context

logger = get_logger(__name__)

class OrderService:
    """
    Servicio de Órdenes - Capa de Aplicación
    Contiene toda la lógica de negocio relacionada con órdenes
    """
    FREE_SHIPPING_THRESHOLD = Decimal("500.00")
    DEFAULT_SHIPPING_COST = Decimal("50.00")
    
    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        product_repository: ProductRepositoryPort,
        cart_repository: Optional[CartRepositoryPort] = None,
        tax_rate: Decimal = Decimal("0.21")
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.cart_repository = cart_repository
        self.tax_rate = tax_rate

    # ==================== CREATE ORDER ====================
    def create_order_from_cart(
        self, user_id: int, cart_id: int, 
        shipping_address: str, billing_address: str,
        notes: Optional[str] = None
    ) -> Order:
        try:
            """
            Crea una orden desde un carrito de compras.
            
            Proceso:
            1. Validar carrito y productos
            2. Verificar stock disponible
            3. Reducir stock de productos
            4. Crear orden con snapshot de datos
            5. Limpiar carrito
            """
            # 1. Obtener carrito
            if not self.cart_repository:
                raise BusinessRuleException("Cart repository no configurado")
            
            cart = self.cart_repository.find_by_id(cart_id)
            if not cart:
                raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
            
            if cart.user_id != user_id:
                raise BusinessRuleException("No autorizado para acceder a este carrito")
            
            if not cart.items:
                raise BusinessRuleException("El carrito está vacío")
            
            # 2. Validar productos y stock, preparar items de orden
            order_items = []
            for cart_item in cart.items:
                product = self.product_repository.find_by_id(cart_item.product_id)
                if not product:
                    raise EntityNotFoundException(f"Producto {cart_item.product_id} no encontrado")
                if not product.is_available:
                    raise BusinessRuleException(f"'{product.name}' ya no está disponible")
                if product.stock < cart_item.quantity:
                    raise InsufficientStockException(
                        f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}"
                    )
                # Crear item de orden con snapshot de datos
                order_item = OrderItem(
                    id=None,
                    product_id=product.id,
                    product_name=product.name,  # Snapshot del nombre
                    product_sku=product.sku,     # Snapshot del SKU
                    quantity=cart_item.quantity,
                    unit_price=product.final_price,  # Snapshot del precio
                    total_price=product.final_price * cart_item.quantity
                )
                order_items.append(order_item)
            # 3. Reducir stock de todos los productos
            for cart_item in cart.items:
                product = self.product_repository.find_by_id(cart_item.product_id)
                if product:
                    product.reduce_stock(cart_item.quantity)
                    self.product_repository.save(product)
            # 4. Calcular totales
            subtotal = sum(item.total_price for item in order_items)
            tax_amount = subtotal * self.tax_rate
            shipping_cost = Decimal("0") if subtotal >= self.FREE_SHIPPING_THRESHOLD else self.DEFAULT_SHIPPING_COST
            discount_amount = Decimal("0")  # TODO: Integrar con coupon_service
            total_amount = subtotal + tax_amount + shipping_cost - discount_amount
            # 5. Generar número de orden único
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            # 6. Crear entidad de orden
            order = Order(
                id=None,
                order_number=order_number,
                user_id=user_id,
                status=OrderStatus.PENDING,
                shipping_address=shipping_address,
                billing_address=billing_address,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_cost=shipping_cost,
                discount_amount=discount_amount,
                total_amount=total_amount,
                items=order_items,
                notes=notes
            )
            # 7. Agregar historial inicial
            order.add_status_history(OrderStatus.PENDING, comment="Orden creada desde carrito")
            # 8. Guardar orden
            order = self.order_repository.save(order)
            # 9. Limpiar carrito
            if self.cart_repository:
                self.cart_repository.clear_items(cart_id)
            # ✅ LOGGING: Orden creada desde carrito (evento de negocio)
            logger.info(
                "Orden creada desde carrito",
                extra={
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "user_id": user_id,
                    "cart_id": cart_id,
                    "total": float(order.total_amount),
                    "items_count": len(order.items),
                    "currency": order.currency.value
                }
            )
            
            return order
            
        except (EntityNotFoundException, ValidationError, BusinessRuleException, InsufficientStockException) as e:
            # ✅ LOGGING: Errores de negocio esperados (warning, no error)
            logger.warning(
                f"Error de negocio al crear orden desde carrito: {e}",
                extra={
                    "user_id": user_id,
                    "cart_id": cart_id,
                    "error_type": type(e).__name__,
                    "component": "create_order_from_cart"
                }
            )
            raise
        except Exception as e:
            # ✅ LOGGING: Error inesperado con traceback completo
            logger.exception(
                "Error inesperado al crear orden desde carrito",
                extra={
                    "user_id": user_id,
                    "cart_id": cart_id,
                    "error_type": type(e).__name__,
                    "component": "create_order_from_cart"
                }
            )
            raise

    def create_order_direct(
        self, user_id: int, 
        items: List[Dict[str, Any]],
        shipping_address: str, 
        billing_address: str,                          
        notes: Optional[str] = None
    ) -> Order:
        try:
            """
            Crea una orden directamente (sin carrito), útil para compras rápidas.
            items: [{"product_id": 1, "quantity": 2}, ...]
            """
            # Validar y preparar items
            order_items = []
            for item_data in items:
                product = self.product_repository.find_by_id(item_data["product_id"])
                if not product:
                    raise EntityNotFoundException(f"Producto {item_data['product_id']} no encontrado")
                if not product.is_available:
                    raise BusinessRuleException(f"'{product.name}' ya no está disponible")
                if product.stock < item_data["quantity"]:
                    raise InsufficientStockException(
                        f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}"
                    )
                order_item = OrderItem(
                    id=None,
                    product_id=product.id,
                    product_name=product.name,
                    product_sku=product.sku,
                    quantity=item_data["quantity"],
                    unit_price=product.final_price,
                    total_price=product.final_price * item_data["quantity"]
                )
                order_items.append(order_item)
            # Reducir stock
            for item_data in items:
                product = self.product_repository.find_by_id(item_data["product_id"])
                if product:
                    product.reduce_stock(item_data["quantity"])
                    self.product_repository.save(product)
            # Calcular totales y crear orden (igual que create_order_from_cart)
            subtotal = sum(item.total_price for item in order_items)
            tax_amount = subtotal * self.tax_rate
            shipping_cost = Decimal("0") if subtotal >= self.FREE_SHIPPING_THRESHOLD else self.DEFAULT_SHIPPING_COST
            total_amount = subtotal + tax_amount + shipping_cost
            
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            
            order = Order(
                id=None,
                order_number=order_number,
                user_id=user_id,
                status=OrderStatus.PENDING,
                shipping_address=shipping_address,
                billing_address=billing_address,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_cost=shipping_cost,
                total_amount=total_amount,
                items=order_items,
                notes=notes
            )
            
            order.add_status_history(OrderStatus.PENDING, comment="Orden creada directamente")
            order = self.order_repository.save(order)
            # ✅ LOGGING: Orden creada directamente (evento de negocio)
            logger.info(
                "Orden creada directamente",
                extra={
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "user_id": user_id,
                    "total": float(order.total_amount),
                    "items_count": len(order.items),
                    "currency": order.currency.value
                }
            )
            
            return order
            
        except (EntityNotFoundException, ValidationError, BusinessRuleException, InsufficientStockException) as e:
            logger.warning(
                f"Error de negocio al crear orden directa: {e}",
                extra={
                    "user_id": user_id,
                    "error_type": type(e).__name__,
                    "component": "create_order_direct"
                }
            )
            raise
        except Exception as e:
            logger.exception(
                "Error inesperado al crear orden directa",
                extra={
                    "user_id": user_id,
                    "error_type": type(e).__name__,
                    "component": "create_order_direct"
                }
            )
            raise

    # ==================== READ ORDERS ====================
    
    def get_order(self, order_id: int, user_id: Optional[int] = None) -> Order:
        """Obtiene una orden por ID, con validación de autorización"""
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Orden {order_id} no encontrada")
        
        # Validar que el usuario pueda ver esta orden
        if user_id and order.user_id != user_id:
            # Solo admins pueden ver órdenes de otros usuarios (validar en router)
            raise BusinessRuleException("No autorizado para ver esta orden")
        
        return order

    def get_order_by_number(self, order_number: str, user_id: Optional[int] = None) -> Order:
        """Obtiene una orden por número de orden"""
        order = self.order_repository.find_by_order_number(order_number)
        if not order:
            raise EntityNotFoundException(f"Orden {order_number} no encontrada")
        
        if user_id and order.user_id != user_id:
            raise BusinessRuleException("No autorizado para ver esta orden")
        
        return order

    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100,
                       status: Optional[OrderStatus] = None) -> List[Order]:
        """Obtiene las órdenes de un usuario"""
        return self.order_repository.find_by_user_id(user_id, skip=skip, limit=limit, status=status)

    def get_admin_orders(self, skip: int = 0, limit: int = 100,
                        user_id: Optional[int] = None,
                        status: Optional[OrderStatus] = None,
                        date_from: Optional[str] = None,
                        date_to: Optional[str] = None) -> List[Order]:
        """Obtiene órdenes para admin con filtros avanzados"""
        return self.order_repository.find_all(
            skip=skip, limit=limit, user_id=user_id, 
            status=status, date_from=date_from, date_to=date_to
        )

    def get_pending_orders(self, limit: int = 100) -> List[Order]:
        """Obtiene órdenes pendientes de procesamiento (para admin)"""
        return self.order_repository.find_pending_orders(limit=limit)

    # ==================== UPDATE ORDER STATUS ====================
    
    def confirm_order(self, order_id: int, commented_by: Optional[int] = None) -> Order:
        order = self.get_order(order_id)
        old_status = order.status.value
        
        order.confirm(commented_by)
        order = self.order_repository.save(order)
        
        # ✅ LOGGING: Orden confirmada (evento de negocio importante)
        logger.info(
            "Orden confirmada",
            extra={
                "order_id": order.id,
                "order_number": order.order_number,
                "user_id": order.user_id,
                "old_status": old_status,
                "new_status": order.status.value,
                "total": float(order.total_amount),
                "commented_by": commented_by
            }
        )
        
        return order

    def start_processing(self, order_id: int, commented_by: Optional[int] = None) -> Order:
        """Inicia el procesamiento de una orden confirmada"""
        order = self.get_order(order_id)
        order.start_processing(commented_by)
        return self.order_repository.save(order)

    def ship_order(self, order_id: int, tracking_number: Optional[str] = None,
                  commented_by: Optional[int] = None) -> Order:
        """Marca una orden como enviada"""
        order = self.get_order(order_id)
        order.ship(tracking_number, commented_by)
        return self.order_repository.save(order)

    def deliver_order(self, order_id: int, commented_by: Optional[int] = None) -> Order:
        """Marca una orden como entregada"""
        order = self.get_order(order_id)
        order.deliver(commented_by)
        return self.order_repository.save(order)

    def cancel_order(
        self, order_id: int,
        reason: Optional[str] = None,
        commented_by: Optional[int] = None
    ) -> Order:
        try:
            order = self.get_order(order_id)
            old_status = order.status.value            
            # Guardar items antes de cancelar (para restaurar stock)
            items_to_restore = [(item.product_id, item.quantity) for item in order.items]            
            # Cancelar orden
            order.cancel(reason, commented_by)
            order = self.order_repository.save(order)            
            # Restaurar stock de productos
            for product_id, quantity in items_to_restore:
                product = self.product_repository.find_by_id(product_id)
                if product:
                    product.increase_stock(quantity)
                    self.product_repository.save(product)            
            # ✅ LOGGING: Orden cancelada con stock restaurado
            logger.info(
                "Orden cancelada - stock restaurado",
                extra={
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "user_id": order.user_id,
                    "old_status": old_status,
                    "new_status": order.status.value,
                    "reason": reason,
                    "items_restored": len(items_to_restore),
                    "commented_by": commented_by
                }
            )
            
            return order
            
        except OrderAlreadyShippedException as e:
            logger.warning(
                f"No se puede cancelar orden: {e}",
                extra={"order_id": order_id, "error": str(e)}
            )
            raise
        except Exception as e:
            logger.exception(
                "Error inesperado al cancelar orden",
                extra={"order_id": order_id, "error_type": type(e).__name__}
            )
            raise

    def refund_order(
        self, order_id: int, 
        amount: Optional[Decimal] = None,        
        commented_by: Optional[int] = None
    ) -> Order:
        """Procesa un reembolso para una orden"""
        order = self.get_order(order_id)
        order.refund(amount, commented_by)
        return self.order_repository.save(order)

    # ==================== UTILS & REPORTS ====================
    def validate_order_for_payment(self, order_id: int) -> Dict[str, Any]:
        """Valida que una orden esté lista para pago"""
        order = self.get_order(order_id)
        issues = []
        
        if order.status != OrderStatus.PENDING:
            issues.append(f"La orden no está en estado pendiente: {order.status.value}")
        
        for item in order.items:
            product = self.product_repository.find_by_id(item.product_id)
            if not product:
                issues.append(f"Producto {item.product_id} ya no existe")
            elif not product.is_available:
                issues.append(f"'{product.name}' ya no está disponible")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "can_pay": len(issues) == 0,
            "total_amount": float(order.total_amount)
        }

    def get_order_stats(self, user_id: Optional[int] = None, 
                       date_from: Optional[str] = None,
                       date_to: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene estadísticas de órdenes"""
        orders = self.order_repository.find_all(
            user_id=user_id, date_from=date_from, date_to=date_to, limit=10000
        )
        
        total_sales = sum(float(o.total_amount) for o in orders 
                        if o.status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED])
        
        status_counts = {}
        for order in orders:
            status = order.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_orders": len(orders),
            "total_sales": total_sales,
            "status_breakdown": status_counts,
            "average_order_value": total_sales / len(orders) if orders else 0
        }

    def get_revenue_report(self, date_from: str, date_to: str) -> Dict[str, Any]:
        """Reporte de ingresos por período"""
        orders = self.order_repository.find_all(
            date_from=date_from, date_to=date_to, limit=10000
        )
        
        delivered = [o for o in orders if o.status == OrderStatus.DELIVERED]
        revenue = sum(float(o.total_amount) for o in delivered)
        
        return {
            "period": {"from": date_from, "to": date_to},
            "total_orders": len(orders),
            "delivered_orders": len(delivered),
            "total_revenue": revenue,
            "average_ticket": revenue / len(delivered) if delivered else 0
        }