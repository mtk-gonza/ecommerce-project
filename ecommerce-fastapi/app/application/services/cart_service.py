from typing import Optional
from app.domain.entities.cart import Cart
from app.domain.ports.cart_repository import CartRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.exceptions import EntityNotFoundException, InsufficientStockException, ValidationError

class CartService:
    def __init__(self, cart_repository: CartRepositoryPort, product_repository: ProductRepositoryPort):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def get_or_create_cart(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Cart:
        """Obtiene o crea un carrito"""
        return self.cart_repository.find_or_create(user_id=user_id, session_id=session_id)

    def add_to_cart(self, cart: Cart, product_id: int, quantity: int) -> Cart:
        """Agrega un producto al carrito"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException(f"Producto {product_id} no encontrado")
        
        if product.stock < quantity:
            raise InsufficientStockException(f"Stock insuficiente para {product.name}")
        
        # Usar método optimizado del repositorio
        cart = self.cart_repository.add_item(
            cart_id=cart.id,
            product_id=product_id,
            product_name=product.name,
            product_sku=product.sku,
            quantity=quantity,
            unit_price=float(product.final_price)
        )
        return cart

    def remove_from_cart(self, cart: Cart, product_id: int) -> Cart:
        """Remueve un item del carrito"""
        cart = self.cart_repository.remove_item(cart.id, product_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito no encontrado")
        return cart

    def update_item_quantity(self, cart: Cart, product_id: int, quantity: int) -> Cart:
        """Actualiza la cantidad de un item"""
        cart = self.cart_repository.update_item_quantity(cart.id, product_id, quantity)
        if not cart:
            raise EntityNotFoundException(f"Carrito no encontrado")
        return cart

    def clear_cart(self, cart: Cart) -> Cart:
        """Vacía el carrito"""
        self.cart_repository.clear_items(cart.id)
        return self.cart_repository.find_by_id(cart.id)

    def get_cart_subtotal(self, cart_id: int) -> float:
        """Obtiene el subtotal del carrito"""
        return self.cart_repository.get_subtotal(cart_id)

    def get_cart_item_count(self, cart_id: int) -> int:
        """Obtiene la cantidad total de items"""
        return self.cart_repository.get_item_count(cart_id)

    def delete_cart(self, cart_id: int) -> bool:
        """Elimina el carrito"""
        return self.cart_repository.delete(cart_id)