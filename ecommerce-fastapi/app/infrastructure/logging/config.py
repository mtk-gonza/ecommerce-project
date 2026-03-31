import logging
import sys
from pathlib import Path
from typing import Optional
from .handlers import get_console_handler, get_file_handler, get_webhook_handler

def setup_logging(
    env: str = "dev",
    log_level: str = "INFO",
    log_dir: str | Path = "logs",
    enable_file_logging: bool = True,
    enable_webhook_logging: bool = True,
) -> None:
    """
    Configura el logging para toda la aplicación.
    
    Args:
        env: Entorno ('dev', 'staging', 'prod')
        log_level: Nivel mínimo de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        log_dir: Directorio para archivos de log
        enable_file_logging: Si habilitar logs en archivo
        enable_webhook_logging: Si habilitar log separado para webhooks
    """
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Limpiar handlers existentes (evitar duplicados en reload)
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # Console handler (siempre habilitado)
    use_colors = env == "dev" and sys.stdout.isatty()
    console_handler = get_console_handler(log_level, use_colors=use_colors)
    root_logger.addHandler(console_handler)
    
    # File handler (opcional, recomendado para prod)
    if enable_file_logging:
        log_path = Path(log_dir) / "app.log"
        use_json = env != "dev"  # JSON solo en prod/staging
        file_handler = get_file_handler(
            log_path=log_path,
            log_level=log_level,
            use_json=use_json
        )
        root_logger.addHandler(file_handler)
    
    # Webhook handler (opcional, útil para debugging de pagos)
    if enable_webhook_logging:
        webhook_handler = get_webhook_handler(
            log_path=log_dir,
            log_level="INFO"  # Siempre INFO para webhooks, sin importar log_level global
        )
        # Agregar filtro para solo logs de webhooks
        webhook_handler.addFilter(lambda record: "webhook" in record.name.lower())
        root_logger.addHandler(webhook_handler)
    
    # Configurar loggers de terceros (silenciar demasiado verbose)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # En dev, mostrar SQL para debugging (opcional)
    if env == "dev" and log_level == "DEBUG":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    
    # Log de inicio
    logger = logging.getLogger(__name__)
    logger.info(f"🔧 Logging configurado: env={env}, level={log_level}, dir={log_dir}")


def get_log_config(
    env: str = "dev",
    log_level: str = "INFO",
) -> dict:
    """
    Retorna configuración de logging compatible con Uvicorn/FastAPI.
    Útil para pasar a uvicorn.run(log_config=...)
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": env == "dev",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": log_level},
            "uvicorn.error": {"level": log_level},
            "uvicorn.access": {"handlers": ["access"], "level": log_level, "propagate": False},
        },
    }