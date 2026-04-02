# tests/test_payment_service.py

import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from app.application.services.payment_service import PaymentService
from app.domain.entities.payment import Payment
from app.domain.entities.order import Order, OrderItem
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency, OrderStatus
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    PaymentProcessingException
)

# ==================== FIXTURES ====================

@pytest.fixture
def mock_payment_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_order_id = Mock(return_value=None)
    repo.find_by_mp_payment_id = Mock(return_value=None)
    repo.save = Mock(side_effect=lambda p: p)
    return repo

@pytest.fixture
def mock_order_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.save = Mock(side_effect=lambda o: o)
    return repo

@pytest.fixture
def mock_mp_client():
    client = Mock()
    client.create_preference = Mock(return_value={
        "success": True,
        "data": {"id": "pref_12345", "init_point": "https://sandbox.mercadopago.com/checkout"},
        "sandbox_init_point": "https://sandbox.mercadopago.com/checkout"
    })
    client.create_payment = Mock(return_value={
        "success": True,
        "data": {"id": "pay_12345", "status": "approved"},
        "payment_id": "pay_12345",
        "status": "approved"
    })
    client.get_payment = Mock(return_value={
        "success": True,
        "data": {"id": "pay_12345", "status": "approved", "transaction_amount": 100.00}
    })
    return client

@pytest.fixture
def payment_service(mock_payment_repository, mock_order_repository, mock_mp_client):
    return PaymentService(
        payment_repository=mock_payment_repository,
        order_repository=mock_order_repository,
        mercadopago_client=mock_mp_client
    )

@pytest.fixture
def sample_order():
    return Order(
        id=1, order_number="ORD-20240329-ABC123", user_id=1,
        status=OrderStatus.PENDING,
        subtotal=Decimal("199.98"),
        tax_amount=Decimal("31.99"),
        shipping_cost=Decimal("50.00"),
        total_amount=Decimal("281.97"),
        currency=Currency.USD,
        items=[
            OrderItem(
                id=1, product_id=1, product_name="Producto Test",
                product_sku="PROD-001", quantity=2,
                unit_price=Decimal("99.99"), total_price=Decimal("199.98")
            )
        ]
    )

# ==================== TESTS: CREATE PAYMENT PREFERENCE ====================

class TestPaymentServicePreference:
    
    def test_create_payment_preference_success(self, payment_service, mock_order_repository, 
                                              mock_payment_repository, mock_mp_client, sample_order):
        """Crear preferencia de pago exitosamente"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        mock_payment_repository.find_by_order_id.return_value = None
        
        # Act
        result = payment_service.create_payment_preference(
            order_id=1,
            user_data={"email": "user@example.com", "name": "Test User"}
        )
        
        # Assert
        assert result["success"] == True
        assert "init_point" in result
        assert result["amount"] == 281.97
        mock_mp_client.create_preference.assert_called_once()
        mock_payment_repository.save.assert_called()
    
    def test_create_payment_preference_order_not_found(self, payment_service, mock_order_repository):
        """Error: orden no encontrada"""
        # Arrange
        mock_order_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(EntityNotFoundException, match="Orden"):
            payment_service.create_payment_preference(999, {"email": "test@test.com"})
    
    def test_create_payment_preference_order_already_paid(self, payment_service, 
                                                         mock_order_repository, mock_payment_repository, sample_order):
        """Error: orden ya pagada"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        existing_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.APPROVED, amount=Decimal("100")
        )
        mock_payment_repository.find_by_order_id.return_value = existing_payment
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="ya está pagada"):
            payment_service.create_payment_preference(1, {"email": "test@test.com"})
    
    def test_create_payment_preference_mercadopago_error(self, payment_service,
                                                        mock_order_repository, mock_payment_repository, 
                                                        mock_mp_client, sample_order):
        """Error: fallo en API de MercadoPago"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        mock_payment_repository.find_by_order_id.return_value = None
        mock_mp_client.create_preference.return_value = {
            "success": False,
            "error": "Invalid currency"
        }
        
        # Act & Assert
        with pytest.raises(PaymentProcessingException, match="Error al crear preferencia"):
            payment_service.create_payment_preference(1, {"email": "test@test.com"})

# ==================== TESTS: DIRECT PAYMENT ====================

class TestPaymentServiceDirect:
    
    def test_create_direct_payment_success(self, payment_service, mock_order_repository,
                                          mock_payment_repository, mock_mp_client, sample_order):
        """Crear pago directo exitosamente"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        payment_data = {
            "token": "tok_abc123",
            "payment_method_id": "visa",
            "installments": 1
        }
        
        # Act
        result = payment_service.create_direct_payment(
            order_id=1,
            payment_data=payment_data,
            user_data={"email": "user@example.com"}
        )
        
        # Assert
        assert result["success"] == True
        assert result["status"] == "approved"
        mock_mp_client.create_payment.assert_called_once()
    
    def test_create_direct_payment_card_declined(self, payment_service, mock_order_repository,
                                                mock_payment_repository, mock_mp_client, sample_order):
        """Error: tarjeta rechazada"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        mock_mp_client.create_payment.return_value = {
            "success": False,
            "error": "card rejected",
            "error_type": "CARD_REJECTED"
        }
        
        # Act & Assert
        with pytest.raises(PaymentProcessingException, match="Error al procesar pago"):
            payment_service.create_direct_payment(
                order_id=1,
                payment_data={"token": "tok_bad", "payment_method_id": "visa"},
                user_data={"email": "user@example.com"}
            )

# ==================== TESTS: WEBHOOK ====================

class TestPaymentServiceWebhook:
    
    def test_handle_webhook_payment_approved(self, payment_service, mock_payment_repository, mock_mp_client):
        """Procesar webhook de pago aprobado"""
        # Arrange
        existing_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.PENDING, 
            mp_payment_id="pay_12345", amount=Decimal("100")
        )
        mock_payment_repository.find_by_mp_payment_id.return_value = existing_payment
        
        # Act
        result = payment_service.handle_webhook(
            topic="payment",
            payment_data={"id": "pay_12345"}
        )
        
        # Assert
        assert result["success"] == True
        assert existing_payment.status == PaymentStatus.APPROVED
        mock_payment_repository.save.assert_called()
    
    def test_handle_webhook_unknown_payment(self, payment_service, mock_payment_repository):
        """Webhook para pago no registrado en nuestro sistema"""
        # Arrange
        mock_payment_repository.find_by_mp_payment_id.return_value = None
        
        # Act
        result = payment_service.handle_webhook(
            topic="payment",
            payment_data={"id": "pay_unknown"}
        )
        
        # Assert
        assert result["success"] == True  # No es error, solo no lo encontramos
        assert "no encontrado" in result["message"].lower()

# ==================== TESTS: REFUND & CANCEL ====================

class TestPaymentServiceRefundCancel:
    
    def test_refund_payment_success(self, payment_service, mock_payment_repository, mock_mp_client):
        """Reembolsar pago exitosamente"""
        # Arrange
        approved_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.APPROVED,
            mp_payment_id="pay_12345", amount=Decimal("100")
        )
        mock_payment_repository.find_by_id.return_value = approved_payment
        mock_mp_client.refund_payment.return_value = {"success": True, "refund_id": "ref_123"}
        
        # Act
        result = payment_service.refund_payment(1)
        
        # Assert
        assert result.status == PaymentStatus.REFUNDED
        mock_mp_client.refund_payment.assert_called_once()
    
    def test_refund_payment_not_approved(self, payment_service, mock_payment_repository):
        """Error: reembolsar pago no aprobado"""
        # Arrange
        pending_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.PENDING, amount=Decimal("100")
        )
        mock_payment_repository.find_by_id.return_value = pending_payment
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="No se puede reembolsar"):
            payment_service.refund_payment(1)
    
    def test_cancel_payment_success(self, payment_service, mock_payment_repository, mock_mp_client):
        """Cancelar pago pendiente"""
        # Arrange
        pending_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.PENDING,
            mp_payment_id="pay_12345", amount=Decimal("100")
        )
        mock_payment_repository.find_by_id.return_value = pending_payment
        
        # Act
        result = payment_service.cancel_payment(1, reason="Usuario canceló")
        
        # Assert
        assert result.status == PaymentStatus.CANCELLED
        assert result.last_error == "Usuario canceló"
    
    def test_cancel_payment_already_completed(self, payment_service, mock_payment_repository):
        """Error: cancelar pago ya completado"""
        # Arrange
        approved_payment = Payment(
            id=1, order_id=1, status=PaymentStatus.APPROVED, amount=Decimal("100")
        )
        mock_payment_repository.find_by_id.return_value = approved_payment
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="No se puede cancelar"):
            payment_service.cancel_payment(1)