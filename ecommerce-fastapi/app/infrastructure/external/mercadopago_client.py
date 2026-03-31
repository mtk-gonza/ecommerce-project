import mercadopago
from typing import Dict, Any, Optional
from decimal import Decimal
from app.config.settings import settings

class MercadoPagoClient:
    """Cliente para integrar con la API de MercadoPago"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.MERCADOPAGO_ACCESS_TOKEN
        self.sdk = mercadopago.SDK(self.access_token)
    
    def create_preference(self, preference_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una preferencia de pago (Checkout Pro)"""
        try:
            result = self.sdk.preference().create(preference_data)
            return {
                "success": True,
                "data": result["response"],
                "init_point": result["response"]["init_point"],
                "sandbox_init_point": result["response"].get("sandbox_init_point"),
                "preference_id": result["response"]["id"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Obtiene detalles de un pago por ID de MercadoPago"""
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
        """Procesa reembolso total o parcial"""
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
    
    @staticmethod
    def get_supported_currencies() -> list:
        return ["ARS", "BRL", "MXN", "COP", "CLP", "PEN", "UYU", "USD"]