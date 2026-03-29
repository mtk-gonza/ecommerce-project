from app.domain.entities.payment import Payment
from app.domain.enums import PaymentStatus
from app.domain.ports.payment_repository import PaymentRepositoryPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.exceptions import EntityNotFoundException, BusinessRuleException

class PaymentService:
    def __init__(self, payment_repository: PaymentRepositoryPort, order_repository: OrderRepositoryPort):
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    def create_payment(self, order_id: int, amount: float, payment_method: str) -> Payment:
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Orden {order_id} no encontrada")
        
        payment = Payment(
            id=None,
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            status=PaymentStatus.PENDING
        )
        return self.payment_repository.save(payment)

    def complete_payment(self, payment_id: int, transaction_id: str) -> Payment:
        payment = self.payment_repository.find_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException(f"Pago {payment_id} no encontrado")
        payment.complete(transaction_id)
        return self.payment_repository.save(payment)

    def refund_payment(self, payment_id: int, amount: float = None) -> Payment:
        payment = self.payment_repository.find_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException(f"Pago {payment_id} no encontrado")
        payment.refund(amount)
        return self.payment_repository.save(payment)