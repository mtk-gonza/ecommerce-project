# tests/test_cart_service.py

import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from app.application.services.cart_service import CartService
from app.domain.entities.cart import Cart, CartItem
from app.domain.entities.product import Product
from app.domain.enums import ProductStatus, Currency
from app.domain.exceptions import EntityNotFoundException, ValidationError, InsufficientStockException, BusinessRuleException

# ==================== FIXTURES ====================

@pytest.fixture
def mock_cart_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_user_id = Mock(return_value=None)
    repo.find_by_session_id = Mock(return_value=None)
    repo.save = Mock(side_effect=lambda c: c)
    repo.delete = Mock(return_value=True)
    return repo

@pytest.fixture
def mock_product_repository():
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_sku = Mock(return_value=None)
    repo.find_by_slug = Mock(return_value=None)
    repo.find_all = Mock(return_value=[])
    repo.save = Mock(side_effect=lambda p: p)
    return repo

@pytest.fixture
def cart_service(mock_cart_repository, mock_product_repository):
    return CartService(
        cart_repository=mock_cart_repository,
        product_repository=mock_product_repository
    )

@pytest.fixture
def sample_cart():
    return Cart(id=1, user_id=1, session_id=None, items=[])

@pytest.fixture
def sample_product():
    return Product(
        id=1, sku="TEST-001", slug="test-product", name="Producto Test",
        description="Descripción", base_price=Decimal("99.99"),
        stock=10, low_stock_threshold=5, currency=Currency.USD,
        status=ProductStatus.ACTIVE, is_visible=True
    )

# ==================== TESTS: GET/CREATE CART ====================

class TestCartServiceGetOrCreate:
    
    def test_get_or_create_cart_with_user(self, cart_service, mock_cart_repository, sample_cart):
        """Obtener o crear carrito para usuario registrado"""
        # Arrange
        mock_cart_repository.find_by_user_id.return_value = sample_cart
        
        # Act
        result = cart_service.get_or_create_cart(user_id=1)
        
        # Assert
        assert result.id == 1
        assert result.user_id == 1
        mock_cart_repository.find_by_user_id.assert_called_once_with(1)
    
    def test_get_or_create_cart_creates_new(self, cart_service, mock_cart_repository):
        """Crear nuevo carrito si no existe"""
        # Arrange
        mock_cart_repository.find_by_user_id.return_value = None
        mock_cart_repository.save.side_effect = lambda c: Cart(id=999, **{k:v for k,v in c.__dict__.items() if k != 'id'})
        
        # Act
        result = cart_service.get_or_create_cart(user_id=1)
        
        # Assert
        assert result.id == 999
        assert result.user_id == 1
        mock_cart_repository.save.assert_called_once()
    
    def test_get_or_create_cart_requires_id(self, cart_service):
        """Error: se requiere user_id o session_id"""
        with pytest.raises(ValidationError, match="Se requiere"):
            cart_service.get_or_create_cart()

# ==================== TESTS: ADD TO CART ====================

class TestCartServiceAddItem:
    
    def test_add_to_cart_success(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Agregar producto al carrito exitosamente"""
        # Arrange
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act
        result = cart_service.add_to_cart(1, 1, 2)
        
        # Assert
        assert len(result.items) == 1
        assert result.items[0].quantity == 2
        assert result.items[0].unit_price == Decimal("99.99")
    
    def test_add_to_cart_product_not_found(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart):
        """Error: producto no encontrado"""
        # Arrange
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(EntityNotFoundException, match="Producto"):
            cart_service.add_to_cart(1, 999, 1)
    
    def test_add_to_cart_insufficient_stock(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Error: stock insuficiente"""
        # Arrange
        sample_product.stock = 1
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act & Assert
        with pytest.raises(InsufficientStockException, match="Stock insuficiente"):
            cart_service.add_to_cart(1, 1, 5)
    
    def test_add_to_cart_product_not_available(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Error: producto no disponible"""
        # Arrange
        from app.domain.enums import ProductStatus
        sample_product.status = ProductStatus.INACTIVE
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act & Assert
        with pytest.raises(BusinessRuleException, match="no está disponible"):
            cart_service.add_to_cart(1, 1, 1)
    
    def test_add_to_cart_updates_existing_item(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Actualizar cantidad si producto ya existe en carrito"""
        # Arrange
        sample_cart.items = [CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))]
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act: Agregar 3 más del mismo producto
        result = cart_service.add_to_cart(1, 1, 3)
        
        # Assert: Cantidad debe ser 2+3=5
        assert len(result.items) == 1
        assert result.items[0].quantity == 5

# ==================== TESTS: UPDATE/REMOVE ITEMS ====================

class TestCartServiceUpdateRemove:
    
    def test_update_cart_item_success(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Actualizar cantidad de item exitosamente"""
        # Arrange
        sample_cart.items = [CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))]
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act
        result = cart_service.update_cart_item(1, 1, 5)
        
        # Assert
        assert result.items[0].quantity == 5
    
    def test_update_cart_item_remove_if_zero(self, cart_service, mock_cart_repository, sample_cart):
        """Actualizar a cantidad 0 remueve el item"""
        # Arrange
        sample_cart.items = [CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))]
        mock_cart_repository.find_by_id.return_value = sample_cart
        
        # Act
        result = cart_service.update_cart_item(1, 1, 0)
        
        # Assert
        assert len(result.items) == 0
    
    def test_remove_from_cart_success(self, cart_service, mock_cart_repository, sample_cart):
        """Remover item del carrito"""
        # Arrange
        sample_cart.items = [
            CartItem(id=1, product_id=1, product_name="Test1", product_sku="T1", quantity=1, unit_price=Decimal("10")),
            CartItem(id=2, product_id=2, product_name="Test2", product_sku="T2", quantity=2, unit_price=Decimal("20")),
        ]
        mock_cart_repository.find_by_id.return_value = sample_cart
        
        # Act
        result = cart_service.remove_from_cart(1, 1)
        
        # Assert
        assert len(result.items) == 1
        assert result.items[0].product_id == 2
    
    def test_clear_cart_success(self, cart_service, mock_cart_repository, sample_cart):
        """Vaciar carrito completamente"""
        # Arrange
        sample_cart.items = [CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))]
        mock_cart_repository.find_by_id.return_value = sample_cart
        
        # Act
        result = cart_service.clear_cart(1)
        
        # Assert
        assert len(result.items) == 0

# ==================== TESTS: CART MERGE ====================

class TestCartServiceMerge:
    
    def test_merge_guest_cart_success(self, cart_service, mock_cart_repository, mock_product_repository, sample_product):
        """Fusionar carrito de invitado a usuario"""
        # Arrange
        guest_cart = Cart(id=1, user_id=None, session_id="guest-123", items=[
            CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))
        ])
        user_cart = Cart(id=2, user_id=1, session_id=None, items=[])
        
        mock_cart_repository.find_by_session_id.return_value = guest_cart
        mock_cart_repository.find_by_user_id.return_value = user_cart
        mock_product_repository.find_by_id.return_value = sample_product
        mock_cart_repository.save.side_effect = lambda c: c
        
        # Act
        result = cart_service.merge_guest_cart("guest-123", 1)
        
        # Assert
        assert len(result.items) == 1
        assert result.items[0].quantity == 2
        assert result.user_id == 1
    
    def test_merge_guest_cart_sums_quantities(self, cart_service, mock_cart_repository, mock_product_repository, sample_product):
        """Fusionar: sumar cantidades si mismo producto en ambos carritos"""
        # Arrange
        guest_cart = Cart(id=1, user_id=None, session_id="guest-123", items=[
            CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))
        ])
        user_cart = Cart(id=2, user_id=1, session_id=None, items=[
            CartItem(id=2, product_id=1, product_name="Test", product_sku="TEST-001", quantity=3, unit_price=Decimal("99.99"))
        ])
        
        sample_product.stock = 10  # Suficiente para 2+3=5
        mock_cart_repository.find_by_session_id.return_value = guest_cart
        mock_cart_repository.find_by_user_id.return_value = user_cart
        mock_product_repository.find_by_id.return_value = sample_product
        mock_cart_repository.save.side_effect = lambda c: c
        
        # Act
        result = cart_service.merge_guest_cart("guest-123", 1)
        
        # Assert: 3 + 2 = 5
        assert len(result.items) == 1
        assert result.items[0].quantity == 5

# ==================== TESTS: TOTALS & VALIDATION ====================

class TestCartServiceTotals:
    
    def test_calculate_cart_totals(self, cart_service, sample_cart):
        """Calcular totales del carrito"""
        # Arrange
        sample_cart.items = [
            CartItem(id=1, product_id=1, product_name="P1", product_sku="P1", quantity=2, unit_price=Decimal("10")),
            CartItem(id=2, product_id=2, product_name="P2", product_sku="P2", quantity=1, unit_price=Decimal("20")),
        ]
        
        # Act
        totals = cart_service.calculate_cart_totals(sample_cart)
        
        # Assert
        assert totals["subtotal"] == Decimal("40")  # 2*10 + 1*20
        assert totals["tax_amount"] == Decimal("6.4")  # 40 * 0.16
        assert totals["shipping_cost"] == Decimal("50")  # 40 < 500 threshold
        assert totals["total"] == Decimal("96.4")  # 40 + 6.4 + 50
    
    def test_calculate_cart_totals_free_shipping(self, cart_service, sample_cart):
        """Envío gratis si subtotal >= threshold"""
        # Arrange
        sample_cart.items = [
            CartItem(id=1, product_id=1, product_name="P1", product_sku="P1", quantity=10, unit_price=Decimal("100")),
        ]
        
        # Act
        totals = cart_service.calculate_cart_totals(sample_cart)
        
        # Assert
        assert totals["subtotal"] == Decimal("1000")
        assert totals["shipping_cost"] == Decimal("0")  # 1000 >= 500
        assert totals["total"] == Decimal("1160")  # 1000 + 160 tax + 0 shipping
    
    def test_validate_cart_for_checkout_empty(self, cart_service, mock_cart_repository, sample_cart):
        """Validar carrito vacío para checkout"""
        # Arrange
        mock_cart_repository.find_by_id.return_value = sample_cart
        
        # Act
        result = cart_service.validate_cart_for_checkout(1)
        
        # Assert
        assert result["valid"] == False
        assert "vacío" in result["issues"][0].lower()
    
    def test_validate_cart_for_checkout_success(self, cart_service, mock_cart_repository, mock_product_repository, sample_cart, sample_product):
        """Validar carrito válido para checkout"""
        # Arrange
        sample_cart.items = [CartItem(id=1, product_id=1, product_name="Test", product_sku="TEST-001", quantity=2, unit_price=Decimal("99.99"))]
        mock_cart_repository.find_by_id.return_value = sample_cart
        mock_product_repository.find_by_id.return_value = sample_product
        
        # Act
        result = cart_service.validate_cart_for_checkout(1)
        
        # Assert
        assert result["valid"] == True
        assert result["can_checkout"] == True
        assert len(result["issues"]) == 0