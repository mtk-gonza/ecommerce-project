from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.payment import Payment
from app.domain.ports.payment_repository import PaymentRepositoryPort
from app.infrastructure.db.models.payment_model import PaymentModel
from app.infrastructure.mappers.payment_mapper import PaymentMapper
from app.domain.enums import PaymentStatus

class PaymentRepositoryImpl(PaymentRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, payment: Payment) -> Payment:
        """Crea o actualiza un pago"""
        model = PaymentMapper.to_model(payment)
        
        if payment.id:
            # Actualizar pago existente
            existing = self.db.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
            if existing:
                for key, value in model.__dict__.items():
                    if key not in ['_sa_instance_state', 'id'] and hasattr(existing, key):
                        setattr(existing, key, value)
        else:
            # Crear nuevo pago
            self.db.add(model)
            self.db.flush()
            payment.id = model.id
        
        self.db.commit()
        self.db.refresh(model)
        return PaymentMapper.to_entity(model)

    def find_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca un pago por ID"""
        model = self.db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
        return PaymentMapper.to_entity(model) if model else None

    def find_by_order_id(self, order_id: int) -> Optional[Payment]:
        """Busca el pago de una orden"""
        model = self.db.query(PaymentModel).filter(PaymentModel.order_id == order_id).first()
        return PaymentMapper.to_entity(model) if model else None

    def find_by_external_id(self, external_id: str) -> Optional[Payment]:
        """Busca un pago por ID externo"""
        model = self.db.query(PaymentModel).filter(PaymentModel.external_id == external_id).first()
        return PaymentMapper.to_entity(model) if model else None

    def find_by_mp_payment_id(self, mp_payment_id: str) -> Optional[Payment]:
        """Busca un pago por ID de MercadoPago"""
        model = self.db.query(PaymentModel).filter(PaymentModel.mp_payment_id == mp_payment_id).first()
        return PaymentMapper.to_entity(model) if model else None

    def find_by_status(self, status: PaymentStatus, limit: int = 100) -> List[Payment]:
        """Busca pagos por estado"""
        models = self.db.query(PaymentModel).filter(
            PaymentModel.status == status
        ).order_by(PaymentModel.created_at.desc()).limit(limit).all()
        return [PaymentMapper.to_entity(m) for m in models]

    def find_pending_payments(self, limit: int = 100) -> List[Payment]:
        """Busca pagos pendientes de confirmación"""
        models = self.db.query(PaymentModel).filter(
            PaymentModel.status.in_([PaymentStatus.PENDING, PaymentStatus.IN_PROCESS, PaymentStatus.AUTHORIZED])
        ).order_by(PaymentModel.created_at.asc()).limit(limit).all()
        return [PaymentMapper.to_entity(m) for m in models]

    def delete(self, payment_id: int) -> bool:
        """Elimina un pago (solo si está pendiente o cancelado)"""
        model = self.db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
        if not model:
            return False
        if model.status not in [PaymentStatus.PENDING, PaymentStatus.CANCELLED]:
            return False
        self.db.delete(model)
        self.db.commit()
        return True