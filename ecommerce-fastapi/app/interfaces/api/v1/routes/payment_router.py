from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from typing import Optional
from app.interfaces.api.v1.schemas.payment_schema import (
    PaymentPreferenceCreateSchema,
    PaymentDirectCreateSchema,
    PaymentSchema,
    PaymentPreferenceResponseSchema,
    PaymentDirectResponseSchema,
    PaymentRefundSchema,
    PaymentCancelSchema,
    PaymentResponseSchema,
    PaymentMethodsResponseSchema,
    WebhookNotificationSchema
)
from app.application.services.payment_service import PaymentService
from app.interfaces.api.v1.dependencies.services import get_payment_service
from app.interfaces.api.v1.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions import (
    EntityNotFoundException,
    ValidationError,
    BusinessRuleException,
    PaymentProcessingException
)

router = APIRouter(prefix="/payments", tags=["Payments"])

# ==================== PUBLIC ENDPOINTS ====================

@router.post("/preference", response_model=PaymentPreferenceResponseSchema)
def create_payment_preference(
    payment_data: PaymentPreferenceCreateSchema,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Crea una preferencia de pago en MercadoPago.
    Redirige al usuario a la página de pago de MercadoPago.
    """
    try:
        result = payment_service.create_payment_preference(
            order_id=payment_data.order_id,
            user_data={
                "email": payment_data.payer_email,
                "name": payment_data.payer_name,
                "identification": payment_data.payer_identification
            }
        )
        return result
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PaymentProcessingException as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/direct", response_model=PaymentDirectResponseSchema)
def create_direct_payment(
    payment_data: PaymentDirectCreateSchema,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Crea un pago directo con tarjeta (sin redirección).
    Requiere token generado con MercadoPago.js en el frontend.
    """
    try:
        result = payment_service.create_direct_payment(
            order_id=payment_data.order_id,
            payment_data=payment_data.model_dump(),
            user_data={
                "email": payment_data.payer_email,
                "name": payment_data.payer_name,
                "identification": payment_data.payer_identification
            }
        )
        return result
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PaymentProcessingException as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.get("/methods", response_model=PaymentMethodsResponseSchema)
def get_payment_methods(
    country: str = "AR",
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Obtiene métodos de pago disponibles por país"""
    methods = payment_service.get_payment_methods(country)
    return {
        "success": True,
        "methods": methods,
        "country": country
    }

# ==================== AUTHENTICATED ENDPOINTS ====================

@router.get("/{payment_id}", response_model=PaymentSchema)
def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Obtiene los detalles de un pago"""
    try:
        payment = payment_service.get_payment(payment_id, user_id=current_user.id)
        return payment
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.get("/order/{order_id}", response_model=Optional[PaymentSchema])
def get_payment_by_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Obtiene el pago asociado a una orden"""
    payment = payment_service.get_payment_by_order(order_id, user_id=current_user.id)
    return payment

@router.post("/{payment_id}/refund", response_model=PaymentResponseSchema)
def refund_payment(
    payment_id: int,
    refund_data: PaymentRefundSchema,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Procesa un reembolso (total o parcial)"""
    try:
        # Solo admin o el dueño del pago pueden reembolsar
        payment = payment_service.get_payment(payment_id, user_id=current_user.id)
        result = payment_service.refund_payment(
            payment_id,
            amount=refund_data.amount,
            reason=refund_data.reason
        )
        return {
            "success": True,
            "message": "Reembolso procesado exitosamente",
            "payment": result
        }
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PaymentProcessingException as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/{payment_id}/cancel", response_model=PaymentResponseSchema)
def cancel_payment(
    payment_id: int,
    cancel_data: PaymentCancelSchema,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Cancela un pago pendiente"""
    try:
        payment = payment_service.get_payment(payment_id, user_id=current_user.id)
        result = payment_service.cancel_payment(payment_id, reason=cancel_data.reason)
        return {
            "success": True,
            "message": "Pago cancelado exitosamente",
            "payment": result
        }
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{payment_id}/sync", response_model=PaymentSchema)
def sync_payment_status(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """Sincroniza manualmente el estado de un pago con MercadoPago"""
    try:
        payment = payment_service.get_payment(payment_id, user_id=current_user.id)
        return payment_service.sync_payment_status(payment_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# ==================== WEBHOOK ENDPOINT (Public, no auth) ====================
@router.post("/webhook")
async def handle_mercadopago_webhook(
    request: Request,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Endpoint para recibir notificaciones webhook de MercadoPago.
    """
    try:
        # Parsear cuerpo del webhook
        body = await request.json()
        
        # Extraer tipo y ID
        topic = body.get("type") or body.get("topic")
        data = body.get("data", {})
        payment_id = data.get("id")
        
        if not payment_id:
            return {"success": False, "error": "Payment ID no encontrado"}
        
        # Si es un payment, obtener detalles completos de MP
        if topic == "payment" or "payment" in str(body):
            # Obtener datos actualizados del pago desde MercadoPago
            mp_client = payment_service.mp_client
            mp_result = mp_client.get_payment(str(payment_id))
            
            if mp_result["success"]:
                # Buscar nuestro pago por external_reference o mp_payment_id
                mp_data = mp_result["data"]
                external_ref = mp_data.get("external_reference")
                
                if external_ref:
                    # Buscar por nuestro payment_id
                    payment = payment_service.payment_repository.find_by_id(int(external_ref))
                else:
                    # Buscar por mp_payment_id
                    payment = payment_service.payment_repository.find_by_mp_payment_id(str(payment_id))
                
                if payment:
                    # Actualizar estado
                    payment.update_from_mercadopago(mp_data)
                    payment_service.payment_repository.save(payment)
                    
                    # Si está aprobado, actualizar orden
                    if payment.status.value == "approved":
                        # TODO: Confirmar orden vía OrderService
                        print(f"✅ Pago {payment.id} aprobado - Orden {payment.order_id}")
                
                return {"success": True, "message": "Webhook procesado"}
        
        return {"success": True, "message": "Webhook recibido"}
        
    except Exception as e:
        # Loggear error pero retornar 200
        print(f"❌ Error en webhook: {e}")
        return {"success": False, "error": str(e)}