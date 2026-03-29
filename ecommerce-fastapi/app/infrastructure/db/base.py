from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Obtiene timestamp UTC timezone-aware"""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Mixin con soporte nativo para SQLAlchemy 2.0 Mapped[]"""
    
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=get_utc_now
        )
    
    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            "updated_at", 
            DateTime(timezone=True),
            nullable=False,
            default=get_utc_now,
            onupdate=get_utc_now
        )


Base = declarative_base()