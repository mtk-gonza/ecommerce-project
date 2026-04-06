import logging
from typing import Any, Dict


RESERVED_LOGRECORD_ATTRS = {
    'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
    'filename', 'module', 'lineno', 'funcName', 'created', 'msecs',
    'relativeCreated', 'thread', 'threadName', 'processName',
    'process', 'exc_info', 'exc_text', 'stack_info', 'message'
}


def safe_extra(extra: Dict[str, Any]) -> Dict[str, Any]:
    """Valida que extra no contenga atributos reservados de LogRecord"""
    reserved_found = RESERVED_LOGRECORD_ATTRS & extra.keys()
    if reserved_found:
        raise ValueError(
            f"Los siguientes nombres están reservados en logging.LogRecord: {reserved_found}. "
            f"Usá prefijos como 'user_', 'order_', 'product_', etc."
        )
    return extra


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
    
    ⚠️  Los nombres de los campos NO pueden ser atributos reservados de LogRecord:
        name, msg, args, levelname, filename, lineno, funcName, message, etc.
        Usá prefijos como user_, order_, product_ para evitar conflictos.
    """
    # 1. Validar que extra_fields no contenga atributos reservados de LogRecord
    #    Si hay conflicto, safe_extra() lanza ValueError con mensaje claro
    safe_fields = safe_extra(extra_fields) if extra_fields else {}

    # Mapear nivel de string a método del logger
    level_methods = {
        "debug": logger.debug,
        "info": logger.info,
        "warning": logger.warning,
        "warn": logger.warning,  # alias
        "error": logger.error,
        "exception": logger.exception,
        "critical": logger.critical,
    }

    # 2. Obtener método o fallback a info de logging correspondiente al nivel (info, error, warning, etc.)
    log_method = level_methods.get(level.lower(), logger.info)
    
    # 3. Loggear el mensaje con los campos validados en extra={}
    log_method(message, extra=safe_fields)