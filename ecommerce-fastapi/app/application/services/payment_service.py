import uuid
from typing import Dict, Any, Optional, List
from decimal import Decimal
from datetime import datetime
from app.domain.entities.payment import Payment
from app.domain.entities.order import Order
from app.domain.ports.payment_repository import PaymentRepositoryPort
from app.domain.ports.order_repository import OrderRepositoryPort
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    PaymentProcessingException
)
from app.domain.enums import PaymentStatus, PaymentMethodType, PaymentProvider, Currency
from app.infrastructure.external.mercadopago_client import MercadoPagoClient
from app.config.settings import settings

class PaymentService:
    """
    Servicio de Pagos - Capa de Aplicación
    Integra con MercadoPago para procesar pagos
    """
    
    def __init__(
        self,
        payment_repository: PaymentRepositoryPort,
        order_repository: OrderRepositoryPort,
        mercadopago_client: Optional[MercadoPagoClient] = None
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository
        self.mp_client = mercadopago_client or MercadoPagoClient()
    
    # ==================== CREATE PAYMENT PREFERENCE ====================
    
    def create_payment_preference(self, order_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una preferencia de pago en MercadoPago para checkout con redirección.
        
        Proceso:
        1. Validar orden y monto
        2. Crear registro de pago en BD (estado: pending)
        3. Crear preferencia en MercadoPago
        4. Retornar URL de inicialización para redirigir al usuario
        """
        # 1. Validar orden
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Orden {order_id} no encontrada")
        
        if order.status.value not in ["pending", "confirmed"]:
            raise BusinessRuleException(f"No se puede pagar una orden en estado '{order.status.value}'")
        
        if order.total_amount <= 0:
            raise ValidationError("El monto de la orden debe ser mayor a 0")
        
        # 2. Verificar que no haya un pago existente para esta orden
        existing_payment = self.payment_repository.find_by_order_id(order_id)
        if existing_payment and existing_payment.status == PaymentStatus.APPROVED:
            raise BusinessRuleException("Esta orden ya está pagada")
        
        # 3. Crear registro de pago en BD
        payment = Payment(
            id=None,
            order_id=order_id,
            external_id=f"PAY-{uuid.uuid4().hex[:12].upper()}",
            amount=order.total_amount,
            currency=order.currency,
            status=PaymentStatus.PENDING,
            payer_email=user_data.get("email"),
            payer_name=user_data.get("name"),
            description=f"Pedido #{order.order_number}",
            statement_descriptor=f"ECOMMERCE #{order.order_number[-6:]}",
            back_urls={
                "success": settings.PAYMENT_SUCCESS_URL,
                "pending": settings.PAYMENT_PENDING_URL,
                "failure": settings.PAYMENT_FAILURE_URL
            },
            notification_url=settings.PAYMENT_WEBHOOK_URL
        )
        payment = self.payment_repository.save(payment)
        
        # 4. Preparar items para MercadoPago
        mp_items = [
            {
                "id": str(item.product_id),
                "title": item.product_name[:100],  # Máx 100 chars
                "description": item.product_sku[:250],
                "picture_url": None,  # Opcional: URL de imagen del producto
                "category_id": "others",  # Opcional: categoría de MercadoPago
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "currency_id": order.currency.value
            }
            for item in order.items
        ]
        
        # 5. Preparar datos del pagador
        mp_payer = {
            "email": user_data.get("email"),
            "name": user_data.get("name", "").split()[0] if user_data.get("name") else "Cliente",
            "surname": " ".join(user_data.get("name", "").split()[1:]) if user_data.get("name") else "",
        }
        
        # Agregar identificación si es requerida para el país
        if order.currency.value in ["ARS", "BRL", "MXN"]:
            mp_payer["identification"] = {
                "type": "DNI" if order.currency.value == "ARS" else "CPF" if order.currency.value == "BRL" else "RFC",
                "number": user_data.get("identification", "00000000")  # Validar formato según país
            }
        
        # 6. Crear preferencia en MercadoPago
        preference_data = {
            "items": mp_items,
            "payer": mp_payer,
            "back_urls": payment.back_urls,
            "notification_url": payment.notification_url,
            "external_reference": str(payment.id),  # Nuestro payment_id como referencia
            "statement_descriptor": payment.statement_descriptor,
            "auto_return": "approved",  # Redirigir automáticamente si el pago es aprobado
            "binary_mode": True,  # Aprobar o rechazar inmediatamente
            "expires": False,  # Opcional: hacer que la preferencia expire
            "additional_info": {
                "shipments": {
                    "receiver_address": {
                        "street_name": order.shipping_address[:255],
                        # Agregar más campos de dirección si están disponibles
                    }
                },
                "items": mp_items
            }
        }
        
        # 7. Llamar a API de MercadoPago
        mp_result = self.mp_client.create_preference(preference_data)
        
        if not mp_result["success"]:
            payment.reject(error_code="MP_API_ERROR", error_message=mp_result.get("error"))
            self.payment_repository.save(payment)
            raise PaymentProcessingException(f"Error al crear preferencia en MercadoPago: {mp_result.get('error')}")
        
        # 8. Actualizar pago con IDs de MercadoPago
        mp_data = mp_result["data"]
        payment.external_id = mp_data.get("id")  # ID de la preferencia
        payment = self.payment_repository.save(payment)
        
        # 9. Retornar datos para redirección
        return {
            "success": True,
            "payment_id": payment.id,
            "preference_id": mp_data["id"],
            "init_point": mp_result["sandbox_init_point"] if settings.MERCADOPAGO_SANDBOX else mp_result["init_point"],
            "amount": float(payment.amount),
            "currency": payment.currency.value,
            "expires_at": mp_data.get("expiration_date")
        }
    
    # ==================== CREATE DIRECT PAYMENT ====================
    
    def create_direct_payment(self, order_id: int, payment_data: Dict[str, Any], 
                            user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un pago directo con tarjeta (sin redirección).
        Requiere token de tarjeta generado con MercadoPago.js en el frontend.
        
        payment_data debe incluir:
        - token: token de tarjeta (MP.js)
        - payment_method_id: "visa", "mastercard", etc.
        - installments: cantidad de cuotas
        - issuer_id: ID del banco (opcional)
        """
        # Validaciones similares a create_payment_preference...
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Orden {order_id} no encontrada")
        
        # Crear registro de pago
        payment = Payment(
            id=None,
            order_id=order_id,
            external_id=f"PAY-{uuid.uuid4().hex[:12].upper()}",
            amount=order.total_amount,
            currency=order.currency,
            status=PaymentStatus.IN_PROCESS,  # En proceso mientras se procesa la tarjeta
            payment_method_type=PaymentMethodType.CREDIT_CARD,
            payer_email=user_data.get("email"),
            payer_name=user_data.get("name"),
            description=f"Pedido #{order.order_number}"
        )
        payment = self.payment_repository.save(payment)
        
        # Preparar datos para API de pagos directos
        mp_payment_data = {
            "transaction_amount": float(order.total_amount),
            "token": payment_data["token"],
            "description": payment.description,
            "payment_method_id": payment_data["payment_method_id"],
            "installments": payment_data.get("installments", 1),
            "issuer_id": payment_data.get("issuer_id"),
            "payer": {
                "email": user_data.get("email"),
                "identification": {
                    "type": "DNI",  # Ajustar según país
                    "number": user_data.get("identification", "00000000")
                }
            },
            "external_reference": str(payment.id),
            "notification_url": settings.PAYMENT_WEBHOOK_URL
        }
        
        # Llamar a API de pagos
        mp_result = self.mp_client.create_payment(mp_payment_data)
        
        if not mp_result["success"]:
            payment.reject(
                error_code=mp_result.get("error_type", "MP_ERROR"),
                error_message=mp_result.get("error")
            )
            self.payment_repository.save(payment)
            raise PaymentProcessingException(f"Error al procesar pago: {mp_result.get('error')}")
        
        # Actualizar pago con respuesta de MercadoPago
        mp_data = mp_result["data"]
        payment.update_from_mercadopago(mp_data)
        payment = self.payment_repository.save(payment)
        
        # Si el pago fue aprobado, actualizar estado de la orden
        if payment.is_completed:
            from app.application.services.order_service import OrderService
            # TODO: Integrar con OrderService para confirmar la orden
        
        return {
            "success": True,
            "payment_id": payment.id,
            "mp_payment_id": mp_data["id"],
            "status": payment.status.value,
            "message": "Pago procesado exitosamente" if payment.is_completed else "Pago en proceso"
        }
    
    # ==================== WEBHOOK HANDLER ====================
    
    def handle_webhook(self, topic: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa notificaciones webhook de MercadoPago.
        
        topic: "payment" o "merchant_order"
        payment_data: datos del webhook (sin verificar firma por ahora)
        """
        if topic != "payment":
            return {"success": True, "message": "Topic no soportado"}
        
        # Obtener ID de pago de MercadoPago
        mp_payment_id = payment_data.get("id")
        if not mp_payment_id:
            return {"success": False, "error": "Payment ID no encontrado en webhook"}
        
        # Buscar pago en nuestra BD
        payment = self.payment_repository.find_by_mp_payment_id(str(mp_payment_id))
        if not payment:
            # Podría ser un pago creado fuera de nuestro sistema
            return {"success": True, "message": "Pago no encontrado en nuestro sistema"}
        
        # Obtener datos actualizados del pago desde MercadoPago
        mp_result = self.mp_client.get_payment(str(mp_payment_id))
        if not mp_result["success"]:
            return {"success": False, "error": "No se pudo obtener detalles del pago"}
        
        # Actualizar nuestro registro con los datos de MercadoPago
        payment.update_from_mercadopago(mp_result["data"])
        payment = self.payment_repository.save(payment)
        
        # Si el pago fue aprobado, actualizar la orden
        if payment.is_completed:
            order = self.order_repository.find_by_id(payment.order_id)
            if order and order.status.value == "pending":
                # TODO: Confirmar orden vía OrderService
                pass
        
        return {
            "success": True,
            "payment_id": payment.id,
            "status": payment.status.value,
            "message": "Webhook procesado exitosamente"
        }
    
    # ==================== PAYMENT QUERIES ====================
    
    def get_payment(self, payment_id: int, user_id: Optional[int] = None) -> Payment:
        """Obtiene un pago por ID con validación de autorización"""
        payment = self.payment_repository.find_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException(f"Pago {payment_id} no encontrado")
        
        # Validar que el usuario pueda ver este pago
        if user_id:
            order = self.order_repository.find_by_id(payment.order_id)
            if order and order.user_id != user_id:
                raise BusinessRuleException("No autorizado para ver este pago")
        
        return payment
    
    def get_payment_by_order(self, order_id: int, user_id: Optional[int] = None) -> Optional[Payment]:
        """Obtiene el pago de una orden"""
        payment = self.payment_repository.find_by_order_id(order_id)
        
        if payment and user_id:
            order = self.order_repository.find_by_id(payment.order_id)
            if order and order.user_id != user_id:
                return None  # No autorizado
        
        return payment
    
    def get_user_payments(self, user_id: int, limit: int = 50) -> List[Payment]:
        """Obtiene los pagos de un usuario"""
        # Esto requiere una consulta más compleja que una por order_id
        # Por ahora, retornamos una lista vacía o implementamos un método en el repo
        return []
    
    # ==================== REFUND & CANCEL ====================
    
    def refund_payment(self, payment_id: int, amount: Optional[Decimal] = None, 
                      reason: Optional[str] = None) -> Payment:
        """Procesa un reembolso total o parcial"""
        payment = self.get_payment(payment_id)
        
        if not payment.can_be_refunded:
            raise BusinessRuleException(f"No se puede reembolsar un pago en estado '{payment.status.value}'")
        
        # Procesar reembolso en MercadoPago
        mp_result = self.mp_client.refund_payment(
            payment.mp_payment_id,
            amount if amount else payment.amount
        )
        
        if not mp_result["success"]:
            raise PaymentProcessingException(f"Error al procesar reembolso: {mp_result.get('error')}")
        
        # Actualizar estado local
        payment.refund(amount)
        payment.last_error = reason
        return self.payment_repository.save(payment)
    
    def cancel_payment(self, payment_id: int, reason: Optional[str] = None) -> Payment:
        """Cancela un pago pendiente"""
        payment = self.get_payment(payment_id)
        
        if not payment.is_pending:
            raise BusinessRuleException(f"No se puede cancelar un pago en estado '{payment.status.value}'")
        
        # Cancelar en MercadoPago si tiene mp_payment_id
        if payment.mp_payment_id:
            self.mp_client.cancel_payment(payment.mp_payment_id)
        
        # Actualizar estado local
        payment.cancel(reason)
        return self.payment_repository.save(payment)
    
    # ==================== UTILS ====================
    
    def get_payment_methods(self, country: str = "AR") -> list:
        """Obtiene métodos de pago disponibles por país"""
        return self.mp_client.get_payment_methods(country)
    
    def sync_payment_status(self, payment_id: int) -> Payment:
        """Sincroniza el estado de un pago con MercadoPago"""
        payment = self.get_payment(payment_id)
        
        if not payment.mp_payment_id:
            return payment
        
        mp_result = self.mp_client.get_payment(payment.mp_payment_id)
        if mp_result["success"]:
            payment.update_from_mercadopago(mp_result["data"])
            return self.payment_repository.save(payment)
        
        return payment