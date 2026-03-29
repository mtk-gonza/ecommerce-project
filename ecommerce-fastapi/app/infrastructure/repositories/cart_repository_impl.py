from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.domain.entities.cart import Cart, CartItem
from app.domain.ports.cart_repository import CartRepositoryPort
from app.infrastructure.db.models.cart_model import CartModel, CartItemModel
from app.infrastructure.mappers.cart_mapper import CartMapper
from datetime import datetime

class CartRepositoryImpl(CartRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, cart: Cart) -> Cart:
        """Crea o actualiza un carrito"""
        # Verificar si existe un carrito para este usuario o sesión
        existing_cart = None
        if cart.user_id:
            existing_cart = self.db.query(CartModel).filter(
                CartModel.user_id == cart.user_id
            ).first()
        elif cart.session_id:
            existing_cart = self.db.query(CartModel).filter(
                CartModel.session_id == cart.session_id
            ).first()

        if existing_cart:
            # Actualizar carrito existente
            existing_cart.updated_at = datetime.now()
            cart.id = existing_cart.id
            
            # Eliminar items actuales para reemplazarlos
            self.db.query(CartItemModel).filter(
                CartItemModel.cart_id == existing_cart.id
            ).delete()
        else:
            # Crear nuevo carrito
            cart_model = CartMapper.to_model(cart)
            self.db.add(cart_model)
            self.db.flush()  # Para obtener el ID generado
            cart.id = cart_model.id

        self.db.commit()
        self.db.refresh(cart)
        
        # Guardar items del carrito
        if cart.items:
            for item in cart.items:
                if item.id:
                    # Actualizar item existente
                    item_model = self.db.query(CartItemModel).filter(
                        CartItemModel.id == item.id
                    ).first()
                    if item_model:
                        item_model.product_id = item.product_id
                        item_model.product_name = item.product_name
                        item_model.product_sku = item.product_sku
                        item_model.quantity = item.quantity
                        item_model.unit_price = float(item.unit_price)
                        item_model.updated_at = datetime.now()
                else:
                    # Crear nuevo item
                    item_model = CartMapper.item_to_model(cart.id, item)
                    self.db.add(item_model)
            
            self.db.commit()

        return self.find_by_id(cart.id)

    def find_by_id(self, cart_id: int) -> Optional[Cart]:
        """Busca un carrito por ID"""
        model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        return CartMapper.to_entity(model) if model else None

    def find_by_user_id(self, user_id: int) -> Optional[Cart]:
        """Busca un carrito por user_id"""
        model = self.db.query(CartModel).filter(CartModel.user_id == user_id).first()
        return CartMapper.to_entity(model) if model else None

    def find_by_session_id(self, session_id: str) -> Optional[Cart]:
        """Busca un carrito por session_id (invitados)"""
        model = self.db.query(CartModel).filter(CartModel.session_id == session_id).first()
        return CartMapper.to_entity(model) if model else None

    def find_or_create(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Cart:
        """Busca o crea un carrito"""
        cart = None
        if user_id:
            cart = self.find_by_user_id(user_id)
        elif session_id:
            cart = self.find_by_session_id(session_id)
        
        if not cart:
            cart = Cart(id=None, user_id=user_id, session_id=session_id)
            cart = self.save(cart)
        
        return cart

    def delete(self, cart_id: int) -> bool:
        """Elimina un carrito"""
        model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def clear_items(self, cart_id: int) -> bool:
        """Vacía los items del carrito"""
        cart = self.find_by_id(cart_id)
        if not cart:
            return False
        
        # Eliminar todos los items
        self.db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart_id
        ).delete()
        self.db.commit()
        
        # Actualizar fecha del carrito
        cart_model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        if cart_model:
            cart_model.updated_at = datetime.now()
            self.db.commit()
        
        return True

    def add_item(self, cart_id: int, product_id: int, product_name: str, 
                 product_sku: str, quantity: int, unit_price: float) -> Cart:
        """Agrega un item al carrito"""
        # Verificar si el item ya existe
        existing_item = self.db.query(CartItemModel).filter(
            and_(
                CartItemModel.cart_id == cart_id,
                CartItemModel.product_id == product_id
            )
        ).first()

        if existing_item:
            # Actualizar cantidad
            existing_item.quantity += quantity
            existing_item.updated_at = datetime.now()
        else:
            # Crear nuevo item
            item_model = CartItemModel(
                cart_id=cart_id,
                product_id=product_id,
                product_name=product_name,
                product_sku=product_sku,
                quantity=quantity,
                unit_price=unit_price
            )
            self.db.add(item_model)

        # Actualizar carrito
        cart_model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        if cart_model:
            cart_model.updated_at = datetime.now()

        self.db.commit()
        return self.find_by_id(cart_id)

    def update_item_quantity(self, cart_id: int, product_id: int, quantity: int) -> Cart:
        """Actualiza la cantidad de un item"""
        item_model = self.db.query(CartItemModel).filter(
            and_(
                CartItemModel.cart_id == cart_id,
                CartItemModel.product_id == product_id
            )
        ).first()

        if not item_model:
            raise ValueError("Item no encontrado en el carrito")

        if quantity <= 0:
            # Eliminar item si cantidad es 0 o menor
            self.db.delete(item_model)
        else:
            item_model.quantity = quantity
            item_model.updated_at = datetime.now()

        # Actualizar carrito
        cart_model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        if cart_model:
            cart_model.updated_at = datetime.now()

        self.db.commit()
        return self.find_by_id(cart_id)

    def remove_item(self, cart_id: int, product_id: int) -> Cart:
        """Elimina un item del carrito"""
        item_model = self.db.query(CartItemModel).filter(
            and_(
                CartItemModel.cart_id == cart_id,
                CartItemModel.product_id == product_id
            )
        ).first()

        if item_model:
            self.db.delete(item_model)
            
            # Actualizar carrito
            cart_model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
            if cart_model:
                cart_model.updated_at = datetime.now()
            
            self.db.commit()

        return self.find_by_id(cart_id)

    def get_item_count(self, cart_id: int) -> int:
        """Obtiene la cantidad total de items en el carrito"""
        result = self.db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart_id
        ).all()
        return sum(item.quantity for item in result) if result else 0

    def get_subtotal(self, cart_id: int) -> float:
        """Obtiene el subtotal del carrito"""
        result = self.db.query(CartItemModel).filter(
            CartItemModel.cart_id == cart_id
        ).all()
        return sum(item.quantity * item.unit_price for item in result) if result else 0.0