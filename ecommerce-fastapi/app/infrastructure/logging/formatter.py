import logging
import json
from datetime import datetime
from typing import Any

class ColoredFormatter(logging.Formatter):
    """Formatter con colores para desarrollo (solo en consola)"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Agregar color al nivel
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Agregar nombre del logger en azul
        record.name = f"\033[34m{record.name}\033[0m"
        
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """Formatter JSON para producción (estructurado, parseable)"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar exception si existe
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Agregar campos extra (ej: user_id, order_id, payment_id)
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry, ensure_ascii=False, default=str)