from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.domain.entities.order import Order
from app.domain.ports.order_repository import OrderRepositoryPort
from app.infrastructure.db.models.order_model import OrderModel, OrderItemModel, OrderStatusHistoryModel
from app.infrastructure.mappers.order_mapper import OrderMapper
from app.domain.enums import OrderStatus

class OrderRepositoryImpl(OrderRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, order: Order) -> Order:
        """Crea o actualiza una orden"""
        model = OrderMapper.to_model(order)
        
        if order.id:
            # Actualizar orden existente
            existing = self.db.query(OrderModel).filter(OrderModel.id == order.id).first()
            if existing:
                # Actualizar campos
                for key, value in model.__dict__.items():
                    if key not in ['_sa_instance_state', 'id'] and hasattr(existing, key):
                        setattr(existing, key, value)
                
                # Actualizar items (eliminar y recrear para simplicidad)
                self.db.query(OrderItemModel).filter(OrderItemModel.order_id == order.id).delete()
                if order.items:
                    item_models = OrderMapper.items_to_models(order.id, order.items)
                    self.db.add_all(item_models)
                
                # Actualizar historial
                self.db.query(OrderStatusHistoryModel).filter(OrderStatusHistoryModel.order_id == order.id).delete()
                if order.status_history:
                    history_models = OrderMapper.status_history_to_models(order.id, order.status_history)
                    self.db.add_all(history_models)
        else:
            # Crear nueva orden
            self.db.add(model)
            self.db.flush()  # Obtener ID generado
            order.id = model.id
            
            # Agregar items
            if order.items:
                item_models = OrderMapper.items_to_models(order.id, order.items)
                self.db.add_all(item_models)
            
            # Agregar historial inicial
            if order.status_history:
                history_models = OrderMapper.status_history_to_models(order.id, order.status_history)
                self.db.add_all(history_models)
        
        self.db.commit()
        self.db.refresh(model)
        return OrderMapper.to_entity(model)

    def find_by_id(self, order_id: int, with_items: bool = True, with_history: bool = True) -> Optional[Order]:
        """Busca una orden por ID"""
        query = self.db.query(OrderModel).filter(OrderModel.id == order_id)
        
        if with_items:
            query = query.options(joinedload(OrderModel.items))
        if with_history:
            query = query.options(joinedload(OrderModel.status_history))
        
        model = query.first()
        return OrderMapper.to_entity(model) if model else None

    def find_by_order_number(self, order_number: str, with_items: bool = True) -> Optional[Order]:
        """Busca una orden por número de orden"""
        query = self.db.query(OrderModel).filter(OrderModel.order_number == order_number)
        if with_items:
            query = query.options(joinedload(OrderModel.items))
        model = query.first()
        return OrderMapper.to_entity(model) if model else None

    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100, 
                       status: Optional[OrderStatus] = None,
                       with_items: bool = True) -> List[Order]:  # ✅ AGREGAR with_items como parámetro
        """Busca órdenes de un usuario con filtros"""
        query = self.db.query(OrderModel).filter(OrderModel.user_id == user_id)
        
        if status:
            query = query.filter(OrderModel.status == status)
        
        if with_items:  # ✅ Ahora with_items está definido
            query = query.options(joinedload(OrderModel.items))
        
        models = query.order_by(OrderModel.created_at.desc()).offset(skip).limit(limit).all()
        return [OrderMapper.to_entity(m) for m in models]

    def find_all(self, skip: int = 0, limit: int = 100, 
                user_id: Optional[int] = None,
                status: Optional[OrderStatus] = None,
                date_from: Optional[str] = None,
                date_to: Optional[str] = None,
                with_items: bool = False) -> List[Order]:  # ✅ AGREGAR with_items como parámetro
        """Lista órdenes con filtros avanzados (para admin)"""
        query = self.db.query(OrderModel)
        
        if user_id:
            query = query.filter(OrderModel.user_id == user_id)
        if status:
            query = query.filter(OrderModel.status == status)
        if date_from:
            query = query.filter(OrderModel.created_at >= date_from)
        if date_to:
            query = query.filter(OrderModel.created_at <= date_to)
        
        if with_items:
            query = query.options(joinedload(OrderModel.items))
        
        models = query.order_by(OrderModel.created_at.desc()).offset(skip).limit(limit).all()
        return [OrderMapper.to_entity(m) for m in models]

    def find_pending_orders(self, limit: int = 100, with_items: bool = True) -> List[Order]:  # ✅ AGREGAR with_items
        """Obtiene órdenes pendientes de procesamiento"""
        query = self.db.query(OrderModel).filter(OrderModel.status == OrderStatus.PENDING)
        if with_items:
            query = query.options(joinedload(OrderModel.items))
        models = query.order_by(OrderModel.created_at.asc()).limit(limit).all()
        return [OrderMapper.to_entity(m) for m in models]
    
    def find_by_status(self, status: OrderStatus, limit: int = 100) -> List[Order]:
        """Busca órdenes por estado"""
        models = self.db.query(OrderModel).filter(
            OrderModel.status == status
        ).order_by(OrderModel.created_at.desc()).limit(limit).all()
        return [OrderMapper.to_entity(m) for m in models]

    def delete(self, order_id: int) -> bool:
        """Elimina una orden (solo si está en estado permitido)"""
        model = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not model:
            return False
        # Solo permitir eliminar órdenes canceladas o muy recientes
        if model.status not in [OrderStatus.CANCELLED, OrderStatus.PENDING]:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def count_by_user(self, user_id: int) -> int:
        """Cuenta órdenes de un usuario"""
        return self.db.query(OrderModel).filter(OrderModel.user_id == user_id).count()

    def get_total_sales(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> float:
        """Obtiene total de ventas en un período"""
        query = self.db.query(OrderModel).filter(
            OrderModel.status.in_([OrderStatus.DELIVERED, OrderStatus.SHIPPED])
        )
        if date_from:
            query = query.filter(OrderModel.created_at >= date_from)
        if date_to:
            query = query.filter(OrderModel.created_at <= date_to)
        
        result = query.with_entities(OrderModel.total_amount).all()
        return sum(float(r[0]) for r in result if r[0])