import json
from app.domain.entities.payment import Payment
from app.infrastructure.db.models.payment_model import PaymentModel
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency
from decimal import Decimal

class PaymentMapper:
    @staticmethod
    def to_entity(model: PaymentModel) -> Payment:
        """Convierte modelo SQLAlchemy a entidad de dominio"""
        return Payment(
            id=model.id,
            order_id=model.order_id,
            external_id=model.external_id,
            provider=model.provider,
            amount=Decimal(str(model.amount)),
            currency=model.currency,
            status=model.status,
            payment_method_type=model.payment_method_type,
            payer_email=model.payer_email,
            payer_name=model.payer_name,
            payer_identification=model.payer_identification,
            mp_payment_id=model.mp_payment_id,
            mp_transaction_amount=Decimal(str(model.mp_transaction_amount)) if model.mp_transaction_amount else None,
            mp_installments=model.mp_installments,
            mp_payment_method_id=model.mp_payment_method_id,
            mp_issuer_id=model.mp_issuer_id,
            mp_card_last_four=model.mp_card_last_four,
            date_approved=model.date_approved,
            date_created=model.date_created,
            date_last_updated=model.date_last_updated,
            description=model.description,
            statement_descriptor=model.statement_descriptor,
            notification_url=model.notification_url,
            back_urls=json.loads(model.back_urls) if model.back_urls else {},
            attempts=model.attempts,
            last_error=model.last_error,
            last_error_code=model.last_error_code,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Payment) -> PaymentModel:
        """Convierte entidad de dominio a modelo SQLAlchemy"""
        return PaymentModel(
            id=entity.id,
            order_id=entity.order_id,
            external_id=entity.external_id,
            provider=entity.provider,
            amount=float(entity.amount),
            currency=entity.currency,
            status=entity.status,
            payment_method_type=entity.payment_method_type,
            payer_email=entity.payer_email,
            payer_name=entity.payer_name,
            payer_identification=entity.payer_identification,
            mp_payment_id=entity.mp_payment_id,
            mp_transaction_amount=float(entity.mp_transaction_amount) if entity.mp_transaction_amount else None,
            mp_installments=entity.mp_installments,
            mp_payment_method_id=entity.mp_payment_method_id,
            mp_issuer_id=entity.mp_issuer_id,
            mp_card_last_four=entity.mp_card_last_four,
            date_approved=entity.date_approved,
            date_created=entity.date_created,
            date_last_updated=entity.date_last_updated,
            description=entity.description,
            statement_descriptor=entity.statement_descriptor,
            notification_url=entity.notification_url,
            back_urls=json.dumps(entity.back_urls) if entity.back_urls else None,
            attempts=entity.attempts,
            last_error=entity.last_error,
            last_error_code=entity.last_error_code,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )