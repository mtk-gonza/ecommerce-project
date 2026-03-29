from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.enums import ReviewStatus
from app.domain.exceptions import ValidationError

@dataclass
class Review:
    id: Optional[int]
    product_id: int
    user_id: int
    rating: int
    title: Optional[str] = None
    comment: Optional[str] = None
    status: ReviewStatus = ReviewStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.product_id:
            raise ValidationError("El product_id es obligatorio")
        if not self.user_id:
            raise ValidationError("El user_id es obligatorio")
        if not 1 <= self.rating <= 5:
            raise ValidationError("La calificación debe estar entre 1 y 5")
        if not isinstance(self.status, ReviewStatus):
            raise ValidationError("Estado de reseña inválido")

    def approve(self):
        """Aprueba la reseña"""
        self.status = ReviewStatus.APPROVED
        self.updated_at = datetime.now()

    def reject(self, reason: Optional[str] = None):
        """Rechaza la reseña"""
        self.status = ReviewStatus.REJECTED
        self.updated_at = datetime.now()

    @property
    def is_approved(self) -> bool:
        return self.status == ReviewStatus.APPROVED