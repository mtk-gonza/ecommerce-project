from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.repositories.category_repository_impl import CategoryRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.cart_repository_impl import CartRepositoryImpl
from app.infrastructure.repositories.payment_repository_impl import PaymentRepositoryImpl
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.ports.category_repository import CategoryRepositoryPort
from app.domain.ports.user_repository import UserRepositoryPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.ports.cart_repository import CartRepositoryPort
from app.domain.ports.payment_repository import PaymentRepositoryPort
from .db import get_database_session

def get_product_repository(db: Session = Depends(get_database_session)) -> ProductRepositoryPort:
    return ProductRepositoryImpl(db)

def get_category_repository(db: Session = Depends(get_database_session)) -> CategoryRepositoryPort:
    return CategoryRepositoryImpl(db)

def get_user_repository(db: Session = Depends(get_database_session)) -> UserRepositoryPort:
    return UserRepositoryImpl(db)

def get_order_repository(db: Session = Depends(get_database_session)) -> OrderRepositoryPort:
    return OrderRepositoryImpl(db)

def get_cart_repository(db: Session = Depends(get_database_session)) -> CartRepositoryPort:
    return CartRepositoryImpl(db)

def get_order_repository(db: Session = Depends(get_database_session)) -> OrderRepositoryPort:
    return OrderRepositoryImpl(db)

def get_payment_repository(db: Session = Depends(get_database_session)) -> PaymentRepositoryPort:
    return PaymentRepositoryImpl(db)