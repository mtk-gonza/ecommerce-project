from app.domain.entities.cart import Cart, CartItem
from app.infrastructure.db.models.cart_model import CartModel, CartItemModel
from decimal import Decimal
from typing import List

class CartMapper:
    @staticmethod
    def to_entity(model: CartModel) -> Cart:
        items = [
            CartItem(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=Decimal(str(item.unit_price))
            )
            for item in model.items
        ]
        return Cart(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            items=items,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Cart) -> CartModel:
        model = CartModel(
            id=entity.id,
            user_id=entity.user_id,
            session_id=entity.session_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
        return model

    @staticmethod
    def items_to_models(cart_id: int, items: List[CartItem]) -> List[CartItemModel]:
        return [
            CartItemModel(
                id=item.id,
                cart_id=cart_id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=float(item.unit_price)
            )
            for item in items
        ]

    @staticmethod
    def item_to_model(cart_id: int, item: CartItem) -> CartItemModel:
        return CartItemModel(
            id=item.id,
            cart_id=cart_id,
            product_id=item.product_id,
            product_name=item.product_name,
            product_sku=item.product_sku,
            quantity=item.quantity,
            unit_price=float(item.unit_price)
        )