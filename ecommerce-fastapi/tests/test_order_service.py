import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import Mock, MagicMock
from app.application.services.order_service import OrderService
from app.domain.entities.order import Order, OrderItem, OrderStatusHistory
from app.domain.entities.cart import Cart, CartItem
from app.domain.entities.product import Product
from app.domain.enums import OrderStatus, Currency, ProductStatus
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    InsufficientStockException,
    OrderAlreadyShippedException
)

# ==================== FIXTURES ====================

@pytest.fixture
def mock_order_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_order_number = Mock(return_value=None)
    repo.find_by_user_id = Mock(return_value=[])
    repo.find_all = Mock(return_value=[])
    repo.find_pending_orders = Mock(return_value=[])
    repo.save = Mock(side_effect=lambda o: o)
    repo.delete = Mock(return_value=True)
    return repo

@pytest.fixture
def mock_product_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.save = Mock(side_effect=lambda p: p)
    return repo

@pytest.fixture
def mock_cart_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.clear_items = Mock(return_value=True)
    repo.save = Mock(side_effect=lambda c: c)
    return repo

@pytest.fixture
def order_service(mock_order_repository, mock_product_repository, mock_cart_repository):
    return OrderService(
        order_repository=mock_order_repository,
        product_repository=mock_product_repository,
        cart_repository=mock_cart_repository
    )

@pytest.fixture
def sample_product():
    return Product(
        id=1, sku="PROD-001", slug="producto-test", name="Producto Test",
        description="Descripción", base_price=Decimal("99.99"),
        stock=10, low_stock_threshold=5, currency=Currency.USD,
        status=ProductStatus.ACTIVE, is_visible=True
    )

@pytest.fixture
def sample_cart():
    return Cart(
        id=1, user_id=1, session_id=None,
        items=[
            CartItem(
                id=1, product_id=1, product_name="Producto Test",
                product_sku="PROD-001", quantity=2, unit_price=Decimal("99.99")
            )
        ]
    )

@pytest.fixture
def sample_order():
    return Order(
        id=1, order_number="ORD-20240329-ABC123", user_id=1,
        status=OrderStatus.PENDING,
        shipping_address="Calle Falsa 123",
        billing_address="Calle Falsa 123",
        subtotal=Decimal("199.98"),
        tax_amount=Decimal("31.99"),
        shipping_cost=Decimal("50.00"),
        total_amount=Decimal("281.97"),
        items=[
            OrderItem(
                id=1, product_id=1, product_name="Producto Test",
                product_sku="PROD-001", quantity=2,
                unit_price=Decimal("99.99"), total_price=Decimal("199.98")
            )
        ]
    )

# ==================== TESTS: CREATE ORDER ====================

class TestOrderServiceCreate:
    
    def test_create_order_from_cart_success(self, order_service, mock_order_repository, 
                                           mock_product_repository, mock_cart_repository,
                                           sample_cart, sample_product):
        """Crear orden desde carrito exitosamente"""
        # Arrange
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        mock_order_repository.save.side_effect = lambda o: Order(id=999, **{k:v for k,v in o.__dict__.items() if k != 'id'})
        
        # Act
        result = order_service.create_order_from_cart(
            user_id=1,
            cart_id=1,
            shipping_address="Calle Test 123",
            billing_address="Calle Test 123"
        )
        
        # Assert
        assert result.id == 999
        assert result.status == OrderStatus.PENDING
        assert len(result.items) == 1
        assert result.items[0].quantity == 2
        mock_product_repository.save.assert_called()  # Stock reducido
        mock_cart_repository.clear_items.assert_called_once()
    
    def test_create_order_cart_not_found(self, order_service, mock_cart_repository):
        """Error: carrito no encontrado"""
        # Arrange
        mock_cart_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(EntityNotFoundException, match="Carrito"):
            order_service.create_order_from_cart(1, 999, "addr", "addr")
    
    def test_create_order_unauthorized_cart(self, order_service, mock_cart_repository, sample_cart):
        """Error: usuario no autorizado para carrito"""
        # Arrange
        sample_cart.user_id = 2  # Diferente al user_id pasado
        mock_cart_repository.find_by_id.return_value = sample_cart
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="No autorizado"):
            order_service.create_order_from_cart(1, 1, "addr", "addr")
    
    def test_create_order_empty_cart(self, order_service, mock_cart_repository):
        """Error: carrito vacío"""
        # Arrange
        empty_cart = Cart(id=1, user_id=1, items=[])
        mock_cart_repository.find_by_id.return_value = empty_cart
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="vacío"):
            order_service.create_order_from_cart(1, 1, "addr", "addr")
    
    def test_create_order_product_not_available(self, order_service, mock_cart_repository, 
                                               mock_product_repository, sample_cart, sample_product):
        """Error: producto no disponible"""
        # Arrange
        sample_product.status = ProductStatus.INACTIVE
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="no está disponible"):
            order_service.create_order_from_cart(1, 1, "addr", "addr")
    
    def test_create_order_insufficient_stock(self, order_service, mock_cart_repository,
                                            mock_product_repository, sample_cart, sample_product):
        """Error: stock insuficiente"""
        # Arrange
        sample_product.stock = 1  # Menos que la cantidad del carrito (2)
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act & Assert
        with pytest.raises(InsufficientStockException, match="Stock insuficiente"):
            order_service.create_order_from_cart(1, 1, "addr", "addr")

# ==================== TESTS: READ ORDERS ====================

class TestOrderServiceRead:
    
    def test_get_order_success(self, order_service, mock_order_repository, sample_order):
        """Obtener orden exitosamente"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        
        # Act
        result = order_service.get_order(1, user_id=1)
        
        # Assert
        assert result.id == 1
        assert result.order_number == "ORD-20240329-ABC123"
    
    def test_get_order_not_found(self, order_service, mock_order_repository):
        """Error: orden no encontrada"""
        # Arrange
        mock_order_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(EntityNotFoundException, match="Orden"):
            order_service.get_order(999)
    
    def test_get_order_unauthorized(self, order_service, mock_order_repository, sample_order):
        """Error: usuario no autorizado para ver orden"""
        # Arrange
        sample_order.user_id = 2  # Diferente al user_id pasado
        mock_order_repository.find_by_id.return_value = sample_order
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="No autorizado"):
            order_service.get_order(1, user_id=1)
    
    def test_get_user_orders(self, order_service, mock_order_repository, sample_order):
        """Obtener órdenes de usuario"""
        # Arrange
        mock_order_repository.find_by_user_id.return_value = [sample_order]
        
        # Act
        result = order_service.get_user_orders(user_id=1)
        
        # Assert
        assert len(result) == 1
        assert result[0].id == 1

# ==================== TESTS: UPDATE STATUS ====================

class TestOrderServiceStatus:
    
    def test_confirm_order_success(self, order_service, mock_order_repository, sample_order):
        """Confirmar orden exitosamente"""
        # Arrange
        sample_order.status = OrderStatus.PENDING
        sample_order.status_history = []  # Empezar vacío para test limpio
        mock_order_repository.find_by_id.return_value = sample_order
        mock_order_repository.save.side_effect = lambda o: o

        # Act
        result = order_service.confirm_order(1, commented_by=1)

        # Assert
        assert result.status == OrderStatus.CONFIRMED
        assert len(result.status_history) >= 1  # Al menos la entrada de "Confirmed"
        assert result.status_history[-1].status == OrderStatus.CONFIRMED
        mock_order_repository.save.assert_called_once()
    
    def test_confirm_order_wrong_status(self, order_service, mock_order_repository, sample_order):
        """Error: confirmar orden que no está pendiente"""
        # Arrange
        sample_order.status = OrderStatus.SHIPPED
        mock_order_repository.find_by_id.return_value = sample_order

        # Act & Assert
        # ✅ Regex case-insensitive con (?i)
        with pytest.raises(BusinessRuleException, match=r"(?i)confirmar órdenes pendientes"):
            order_service.confirm_order(1)
    
    def test_cancel_order_success(self, order_service, mock_order_repository, mock_product_repository, sample_order, sample_product):
        """Cancelar orden exitosamente (con restauración de stock)"""
        # Arrange
        sample_order.status = OrderStatus.PENDING
        mock_order_repository.find_by_id.return_value = sample_order
        mock_order_repository.save.side_effect = lambda o: o
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act
        result = order_service.cancel_order(1, reason="Cliente cambió de opinión")
        
        # Assert
        assert result.status == OrderStatus.CANCELLED
        mock_product_repository.save.assert_called()  # Stock restaurado
    
    def test_cancel_order_already_shipped(self, order_service, mock_order_repository, sample_order):
        """Error: cancelar orden ya enviada"""
        # Arrange
        sample_order.status = OrderStatus.SHIPPED
        mock_order_repository.find_by_id.return_value = sample_order
        
        # Act & Assert
        with pytest.raises(OrderAlreadyShippedException):
            order_service.cancel_order(1)

# ==================== TESTS: ADMIN & REPORTS ====================

class TestOrderServiceAdmin:
    
    def test_get_pending_orders(self, order_service, mock_order_repository, sample_order):
        """Obtener órdenes pendientes (admin)"""
        # Arrange
        sample_order.status = OrderStatus.PENDING
        mock_order_repository.find_pending_orders.return_value = [sample_order]
        
        # Act
        result = order_service.get_pending_orders()
        
        # Assert
        assert len(result) == 1
        assert result[0].status == OrderStatus.PENDING
    
    def test_validate_order_for_payment_valid(self, order_service, mock_order_repository, 
                                             mock_product_repository, sample_order, sample_product):
        """Validar orden para pago - válida"""
        # Arrange
        mock_order_repository.find_by_id.return_value = sample_order
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act
        result = order_service.validate_order_for_payment(1)
        
        # Assert
        assert result["valid"] == True
        assert result["can_pay"] == True
    
    def test_get_order_stats(self, order_service, mock_order_repository, sample_order):
        """Obtener estadísticas de órdenes"""
        # Arrange
        sample_order.status = OrderStatus.DELIVERED
        mock_order_repository.find_all.return_value = [sample_order]
        
        # Act
        result = order_service.get_order_stats()
        
        # Assert
        assert result["total_orders"] == 1
        assert result["total_sales"] > 0