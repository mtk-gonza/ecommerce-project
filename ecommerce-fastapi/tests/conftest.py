import pytest
import logging
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, call
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import get_db
from app.application.services.cart_service import CartService

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ==================== LOGGING PARA TESTS ====================

@pytest.fixture(autouse=True)
def configure_logging_for_tests():
    """Configura logging para que los tests no se ensucien con logs"""
    logging.getLogger("app").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    yield
    logging.getLogger("app").setLevel(logging.INFO)


# ==================== DATABASE ====================

@pytest.fixture(scope="function")
def test_db():
    """Fixture para base de datos de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(test_db):
    """Override del dependency get_db para tests"""
    try:
        yield test_db
    finally:
        test_db.close()


# ==================== MOCKS PARA REPOSITORIOS ====================

@pytest.fixture
def mock_cart_repository():
    """Mock del repositorio de carritos"""
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_user_id = Mock(return_value=None)
    repo.find_by_session_id = Mock(return_value=None)
    repo.save = Mock(side_effect=lambda c: c)
    repo.delete = Mock(return_value=True)
    return repo


@pytest.fixture
def mock_product_repository():
    """Mock del repositorio de productos"""
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.find_by_sku = Mock(return_value=None)
    repo.find_by_slug = Mock(return_value=None)
    repo.find_all = Mock(return_value=[])
    repo.save = Mock(side_effect=lambda p: p)
    return repo


# ==================== CART SERVICE FIXTURES ====================

@pytest.fixture
def cart_service(mock_cart_repository, mock_product_repository):
    """
    Fixture de CartService con tax_rate default (21%).
    Para tests que NO dependen del cálculo de impuestos.
    """
    return CartService(
        cart_repository=mock_cart_repository,
        product_repository=mock_product_repository,
        tax_rate=Decimal("0.21")
    )


# ==================== TAX RATE PARAMETRIZADO ====================

@pytest.fixture(params=[
    Decimal("0.16"),  # México/Chile
    Decimal("0.21"),  # Argentina  
    Decimal("0.19"),  # Colombia
], ids=["tax_16", "tax_21", "tax_19"])
def tax_rate_for_totals(request):
    """
    Fixture parametrizado para tax_rate en tests de cálculo de totales.
    """
    return request.param


@pytest.fixture
def cart_service_with_tax(mock_cart_repository, mock_product_repository, tax_rate_for_totals):
    """
    Fixture de CartService con tax_rate parametrizado para tests de totales.
    """
    return CartService(
        cart_repository=mock_cart_repository,
        product_repository=mock_product_repository,
        tax_rate=tax_rate_for_totals
    )