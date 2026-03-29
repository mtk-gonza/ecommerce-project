from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.cart import Cart

class CartRepositoryPort(ABC):
    """Puerto de repositorio de carrito - Define el contrato"""
    
    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        """Crea o actualiza un carrito"""
        pass

    @abstractmethod
    def find_by_id(self, cart_id: int) -> Optional[Cart]:
        """Busca un carrito por ID"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Cart]:
        """Busca un carrito por user_id"""
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Optional[Cart]:
        """Busca un carrito por session_id (invitados)"""
        pass

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        """Elimina un carrito"""
        pass

    @abstractmethod
    def clear_items(self, cart_id: int) -> bool:
        """Vacía los items del carrito"""
        pass