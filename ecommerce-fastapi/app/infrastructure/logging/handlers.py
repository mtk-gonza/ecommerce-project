import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from .formatter import ColoredFormatter, JSONFormatter

def get_console_handler(log_level: str, use_colors: bool = True) -> logging.Handler:
    """Handler para consola con formato legible"""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    if use_colors:
        formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    handler.setFormatter(formatter)
    return handler


def get_file_handler(
    log_path: str | Path,
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    use_json: bool = False
) -> logging.Handler:
    """Handler para archivo con rotación"""
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Rotar por tamaño (RotatingFileHandler) o por tiempo (TimedRotatingFileHandler)
    handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
        delay=True  # No crear el archivo hasta el primer log
    )
    handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    formatter = JSONFormatter() if use_json else logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    return handler


def get_webhook_handler(
    log_path: str | Path,
    log_level: str = "INFO"
) -> logging.Handler:
    """Handler específico para logs de webhooks (fácil de filtrar)"""
    return get_file_handler(
        log_path=Path(log_path) / "webhook.log",
        log_level=log_level,
        use_json=True  # JSON para fácil parsing automático
    )