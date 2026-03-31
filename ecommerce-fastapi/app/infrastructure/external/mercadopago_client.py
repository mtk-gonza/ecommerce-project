import mercadopago
from typing import Dict, Any, Optional
from decimal import Decimal
from app.config.settings import settings

class MercadoPagoClient:
    """
    Cliente para integrar con la API de MercadoPago.
    Documentación: https://www.mercadopago.com.ar/developers/es/reference
    """
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.MERCADOPAGO_ACCESS_TOKEN
        self.sdk = mercadopago.SDK(self.access_token)
        
        # URLs base para preferencias y pagos
        self.base_url = "https://api.mercadopago.com"
    
    def create_preference(self, preference_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una preferencia de pago en MercadoPago.
        
        preference_data debe incluir:
        - items: lista de productos [{id, title, quantity, unit_price, currency_id}]
        - payer: datos del comprador {email, name, identification}
        - back_urls: URLs para redirección {success, pending, failure}
        - notification_url: webhook para notificaciones
        - auto_return: "approved" para redirigir automáticamente
        - payment_methods: métodos permitidos/excluidos
        """
        try:
            result = self.sdk.preference().create(preference_data)
            return {
                "success": True,
                "data": result["response"],
                "init_point": result["response"]["init_point"],  # URL para redirigir al usuario
                "sandbox_init_point": result["response"].get("sandbox_init_point")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def get_preference(self, preference_id: str) -> Dict[str, Any]:
        """Obtiene los detalles de una preferencia"""
        try:
            result = self.sdk.preference().get(preference_id)
            return {
                "success": True,
                "data": result["response"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un pago directo (para pagos con tarjeta sin redirección).
        
        payment_data debe incluir:
        - transaction_amount
        - token: token de tarjeta (generado con MercadoPago.js)
        - description
        - payment_method_id: "visa", "mastercard", etc.
        - installments
        - payer: {email, identification}
        """
        try:
            result = self.sdk.payment().create(payment_data)
            return {
                "success": True,
                "data": result["response"],
                "payment_id": result["response"]["id"],
                "status": result["response"]["status"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Obtiene los detalles de un pago por ID de MercadoPago"""
        try:
            result = self.sdk.payment().get(payment_id)
            return {
                "success": True,
                "data": result["response"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def refund_payment(self, payment_id: str, amount: Optional[Decimal] = None) -> Dict[str, Any]:
        """
        Procesa un reembolso total o parcial.
        
        Si amount es None, se reembolsa el total.
        """
        try:
            refund_data = {}
            if amount is not None:
                refund_data["amount"] = float(amount)
            
            result = self.sdk.refund().create(payment_id, refund_data)
            return {
                "success": True,
                "data": result["response"],
                "refund_id": result["response"]["id"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cancel_payment(self, payment_id: str) -> Dict[str, Any]:
        """Cancela un pago pendiente"""
        try:
            result = self.sdk.payment().cancel(payment_id)
            return {
                "success": True,
                "data": result["response"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_payments(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca pagos con filtros.
        
        params puede incluir:
        - external_reference: nuestro order_id
        - status: estado del pago
        - date_created.from / date_created.to: rango de fechas
        - payer.email: email del comprador
        """
        try:
            result = self.sdk.payment().search(params)
            return {
                "success": True,
                "data": result["response"],
                "total": result["response"]["total"],
                "results": result["response"]["results"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verifica la firma de un webhook de MercadoPago.
        (Opcional, para mayor seguridad)
        """
        # Implementar si se habilita la verificación de firma
        # https://www.mercadopago.com.ar/developers/es/guides/online-payments/checkout-pro/integration#webhooks
        return True  # Por ahora, aceptar todos los webhooks (solo para sandbox)
    
    @staticmethod
    def get_supported_currencies() -> list:
        """Lista de monedas soportadas por MercadoPago"""
        return ["ARS", "BRL", "MXN", "COP", "CLP", "PEN", "UYU", "USD"]
    
    @staticmethod
    def get_payment_methods(country: str = "AR") -> list:
        """
        Obtiene métodos de pago disponibles por país.
        Países: AR, BR, MX, CO, CL, PE, UY
        """
        # Esto podría hacerse vía API, pero por ahora retornamos métodos comunes
        return [
            {"id": "visa", "name": "Visa", "type": "credit_card"},
            {"id": "master", "name": "Mastercard", "type": "credit_card"},
            {"id": "amex", "name": "American Express", "type": "credit_card"},
            {"id": "account_money", "name": "Saldo en cuenta", "type": "account_money"},
            {"id": "rapipago", "name": "RapiPago", "type": "ticket"},
            {"id": "pagofacil", "name": "Pago Fácil", "type": "ticket"},
            {"id": "bancario", "name": "Transferencia bancaria", "type": "bank_transfer"},
        ]