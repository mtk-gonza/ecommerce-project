from fastapi import Depends
# SERVICES
from app.application.services.product_service import ProductService
from app.application.services.user_service import UserService
from app.application.services.order_service import OrderService
from app.application.services.cart_service import CartService
from app.application.services.auth_service import AuthService
from app.application.services.payment_service import PaymentService
# REPOSITORIES PORTS
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.domain.ports.user_repository import UserRepositoryPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.ports.cart_repository import CartRepositoryPort
from app.domain.ports.payment_repository import PaymentRepositoryPort

from app.infrastructure.external.mercadopago_client import MercadoPagoClient
from .repositories import get_product_repository, get_category_repository, get_user_repository, get_order_repository, get_cart_repository, get_payment_repository


def get_user_service(user_repository: UserRepositoryPort = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)

def get_product_service(
    product_repository: ProductRepositoryPort = Depends(get_product_repository),
    category_repository: CategoryRepositoryPort = Depends(get_category_repository)
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        category_repository=category_repository
    )

def get_cart_service(
    cart_repository: CartRepositoryPort = Depends(get_cart_repository),
    product_repository: ProductRepositoryPort = Depends(get_product_repository)
) -> CartService:
    return CartService(
        cart_repository=cart_repository,
        product_repository=product_repository
    )

def get_order_service(
    order_repository: OrderRepositoryPort = Depends(get_order_repository),
    product_repository: ProductRepositoryPort = Depends(get_product_repository),
    cart_repository: CartRepositoryPort = Depends(get_cart_repository)
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        product_repository=product_repository,
        cart_repository=cart_repository
    )

def get_payment_service(
    payment_repository: PaymentRepositoryPort = Depends(get_payment_repository),
    order_repository: OrderRepositoryPort = Depends(get_order_repository)
) -> PaymentService:
    return PaymentService(
        payment_repository=payment_repository,
        order_repository=order_repository,
        mercadopago_client=MercadoPagoClient()
    )