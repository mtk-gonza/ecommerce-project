import logging
from typing import Any, Optional

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre dado.
    
    Uso recomendado:
        logger = get_logger(__name__)
        logger.info("Mensaje", extra={"user_id": 123, "order_id": "ORD-001"})
    """
    return logging.getLogger(name)


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **extra_fields: Any
) -> None:
    """
    Loggear con campos adicionales de contexto (útil para trazabilidad).
    Ejemplo:
        log_with_context(logger, "info", "Pago procesado", 
                        payment_id=123, amount=165.99, status="approved")
    """
    # Crear LogRecord con campos extra
    extra = {"extra_fields": extra_fields} if extra_fields else {}
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message, extra=extra)