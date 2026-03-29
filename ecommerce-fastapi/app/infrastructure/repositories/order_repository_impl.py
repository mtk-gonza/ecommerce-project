import uuid
from decimal import Decimal
from sqlalchemy.orm import Session
from app.infrastructure.logging.logger import get_logger
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.enums import OrderStatus
from app.infrastructure.db.models.order_model import OrderModel, OrderItemModel, OrderStatusHistoryModel
from app.infrastructure.db.models.product_model import ProductModel


logger = get_logger(__name__)

class OrderRepositoryImpl(OrderRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, user_id: int, items: list, shipping_address: dict, billing_address: dict):
        try:
            # Generar número de orden único
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            # Calcular totales
            subtotal = Decimal('0')
            order_items = []
            
            for item in items:
                product = self.db.query(ProductModel).filter(ProductModel.id == item['product_id']).first()
                if not product:
                    raise ValueError(f"Producto {item['product_id']} no existe")
                
                if product.stock_quantity < item['quantity']:
                    raise ValueError(f"Stock insuficiente para {product.name}")
                
                unit_price = product.discount_price or product.base_price
                total_price = unit_price * item['quantity']
                subtotal += total_price
                
                # Reducir stock
                product.stock_quantity -= item['quantity']
                
                order_items.append(OrderItemModel(
                    product_id=product.id,
                    product_name=product.name,
                    product_sku=product.sku,
                    quantity=item['quantity'],
                    unit_price=unit_price,
                    total_price=total_price
                ))
            
            # Obtener estado inicial (ej: Pendiente = 1)
            initial_status = self.db.query(OrderStatusHistoryModel).filter(OrderStatusHistoryModel.status == OrderStatus.PENDING.value).first()
            
            order = OrderModel(
                user_id=user_id,
                order_number=order_number,
                status_id=initial_status.id,
                shipping_address_snapshot=str(shipping_address),
                billing_address_snapshot=str(billing_address),
                subtotal=subtotal,
                tax_amount=subtotal * Decimal('0.16'),  # 16% IVA ejemplo
                shipping_cost=Decimal('50.00'),
                discount_amount=Decimal('0.00'),
                total_amount=subtotal + (subtotal * Decimal('0.16')) + Decimal('50.00'),
                items=order_items
            )
            
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()