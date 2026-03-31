from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from app.domain.entities.cart import Cart, CartItem
from app.domain.ports.cart_repository import CartRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    InsufficientStockException,
    BusinessRuleException
)

class CartService:
    """
    Servicio de Carrito - Capa de Aplicación
    Contiene toda la lógica de negocio relacionada con carritos
    """
    
    TAX_RATE = Decimal("0.16")  # 16% IVA (ajustar según país)
    DEFAULT_SHIPPING_COST = Decimal("50.00")
    FREE_SHIPPING_THRESHOLD = Decimal("500.00")
    
    def __init__(
        self,
        cart_repository: CartRepositoryPort,
        product_repository: ProductRepositoryPort
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    # ==================== GET/CREATE CART ====================
    
    def get_or_create_cart(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Cart:
        """Obtiene o crea un carrito para usuario o invitado"""
        if not user_id and not session_id:
            raise ValidationError("Se requiere user_id o session_id")
        
        # Intentar obtener carrito existente
        if user_id:
            cart = self.cart_repository.find_by_user_id(user_id)
        else:
            cart = self.cart_repository.find_by_session_id(session_id)
        
        # Crear nuevo si no existe
        if not cart:
            cart = Cart(id=None, user_id=user_id, session_id=session_id)
            cart = self.cart_repository.save(cart)
        
        return cart

    def get_cart_summary(self, cart_id: int) -> Dict[str, Any]:
        """Obtiene resumen del carrito para checkout"""
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        subtotal = sum(item.quantity * item.unit_price for item in cart.items)
        tax_amount = subtotal * self.TAX_RATE
        shipping_cost = Decimal("0") if subtotal >= self.FREE_SHIPPING_THRESHOLD else self.DEFAULT_SHIPPING_COST
        discount_amount = Decimal("0")  # TODO: Integrar con coupon_service
        total = subtotal + tax_amount + shipping_cost - discount_amount
        
        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "shipping_cost": shipping_cost,
            "discount_amount": discount_amount,
            "total": total,
            "items_count": sum(item.quantity for item in cart.items),
            "currency": "USD"
        }

    # ==================== ADD/UPDATE/REMOVE ITEMS ====================
    
    def add_to_cart(self, cart_id: int, product_id: int, quantity: int) -> Cart:
        """Agrega un producto al carrito"""
        if quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        # Verificar producto y stock
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException(f"Producto {product_id} no encontrado")
        if not product.is_available:
            raise BusinessRuleException(f"El producto '{product.name}' no está disponible")
        if product.stock < quantity:
            raise InsufficientStockException(f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}")
        
        # Verificar si el producto ya está en el carrito
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)
        
        if existing_item:
            # Actualizar cantidad existente
            new_quantity = existing_item.quantity + quantity
            if product.stock < new_quantity:
                raise InsufficientStockException(f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}")
            existing_item.quantity = new_quantity
        else:
            # Agregar nuevo item
            cart_item = CartItem(
                id=None,
                product_id=product_id,
                product_name=product.name,
                product_sku=product.sku,
                quantity=quantity,
                unit_price=product.final_price
            )
            cart.items.append(cart_item)
        
        cart.updated_at = datetime.now()
        return self.cart_repository.save(cart)

    def update_cart_item(self, cart_id: int, product_id: int, quantity: int) -> Cart:
        """Actualiza la cantidad de un item en el carrito"""
        if quantity <= 0:
            return self.remove_from_cart(cart_id, product_id)
        
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        # Encontrar item
        item = next((item for item in cart.items if item.product_id == product_id), None)
        if not item:
            raise EntityNotFoundException(f"Producto {product_id} no encontrado en el carrito")
        
        # Verificar stock para nueva cantidad
        product = self.product_repository.find_by_id(product_id)
        if product and product.stock < quantity:
            raise InsufficientStockException(f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}")
        
        item.quantity = quantity
        cart.updated_at = datetime.now()
        return self.cart_repository.save(cart)

    def remove_from_cart(self, cart_id: int, product_id: int) -> Cart:
        """Remueve un producto del carrito"""
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        # Filtrar el item a remover
        cart.items = [item for item in cart.items if item.product_id != product_id]
        cart.updated_at = datetime.now()
        return self.cart_repository.save(cart)

    def clear_cart(self, cart_id: int) -> Cart:
        """Vacía completamente el carrito"""
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        cart.items = []
        cart.updated_at = datetime.now()
        return self.cart_repository.save(cart)

    # ==================== CART MERGE (Guest → Registered) ====================
    
    def merge_guest_cart(self, session_id: str, user_id: int) -> Cart:
        """
        Fusiona el carrito de invitado al carrito del usuario registrado.
        Reglas:
        - Si el mismo producto existe en ambos, se suman las cantidades (validando stock)
        - Si hay conflicto de stock, se mantiene la cantidad del usuario registrado
        """
        # Obtener carritos
        guest_cart = self.cart_repository.find_by_session_id(session_id)
        user_cart = self.get_or_create_cart(user_id=user_id)
        
        if not guest_cart or not guest_cart.items:
            return user_cart  # No hay nada que fusionar
        
        # Fusionar items
        for guest_item in guest_cart.items:
            existing_item = next((item for item in user_cart.items if item.product_id == guest_item.product_id), None)
            
            if existing_item:
                # Sumar cantidades, validando stock
                product = self.product_repository.find_by_id(guest_item.product_id)
                if product and product.stock >= (existing_item.quantity + guest_item.quantity):
                    existing_item.quantity += guest_item.quantity
            else:
                # Agregar item nuevo si hay stock
                product = self.product_repository.find_by_id(guest_item.product_id)
                if product and product.stock >= guest_item.quantity and product.is_available:
                    user_cart.items.append(CartItem(
                        id=None,
                        product_id=guest_item.product_id,
                        product_name=guest_item.product_name,
                        product_sku=guest_item.product_sku,
                        quantity=guest_item.quantity,
                        unit_price=guest_item.unit_price
                    ))
        
        user_cart.updated_at = datetime.now()
        user_cart = self.cart_repository.save(user_cart)
        
        # Eliminar carrito de invitado después de fusionar
        if guest_cart.id:
            self.cart_repository.delete(guest_cart.id)
        
        return user_cart

    # ==================== UTILS ====================
    def validate_cart_for_checkout(self, cart_id: int) -> Dict[str, Any]:
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            # Este caso SÍ puede lanzar excepción porque el carrito no existe
            raise EntityNotFoundException(f"Carrito {cart_id} no encontrado")
        
        issues = []
        
        # Validar que no esté vacío
        if not cart.items:
            issues.append("El carrito está vacío")
        
        # Validar cada item
        for item in cart.items:
            product = self.product_repository.find_by_id(item.product_id)
            
            if not product:
                issues.append(f"Producto {item.product_id} ya no existe")
            elif not product.is_available:
                issues.append(f"'{product.name}' ya no está disponible")
            elif product.stock < item.quantity:
                issues.append(f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}, Solicitado: {item.quantity}")
            elif product.final_price != item.unit_price:
                issues.append(f"El precio de '{product.name}' ha cambiado: ${product.final_price}")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "can_checkout": len(issues) == 0,
            "items_count": len(cart.items),
            "total_items": sum(item.quantity for item in cart.items)
        }

    def calculate_cart_totals(self, cart: Cart) -> Dict[str, Decimal]:
        """Calcula todos los totales del carrito"""
        subtotal = sum(item.quantity * item.unit_price for item in cart.items)
        tax_amount = subtotal * self.TAX_RATE
        shipping_cost = Decimal("0") if subtotal >= self.FREE_SHIPPING_THRESHOLD else self.DEFAULT_SHIPPING_COST
        discount_amount = Decimal("0")  # TODO: Integrar coupons
        total = subtotal + tax_amount + shipping_cost - discount_amount
        
        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "shipping_cost": shipping_cost,
            "discount_amount": discount_amount,
            "total": total
        }