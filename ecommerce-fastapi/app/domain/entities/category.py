from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from app.domain.exceptions import ValidationError

@dataclass
class Category:
    id: Optional[int]
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    parent: Optional['Category'] = None
    subcategories: List['Category'] = field(default_factory=list)
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError("El nombre de categoría debe tener al menos 2 caracteres")
        if not self.slug or len(self.slug.strip()) == 0:
            raise ValidationError("El slug es obligatorio")
        if len(self.name) > 100:
            raise ValidationError("El nombre no puede exceder 100 caracteres")

    def add_subcategory(self, category: 'Category'):
        """Agrega una subcategoría"""
        category.parent_id = self.id
        category.parent = self
        self.subcategories.append(category)

    def get_full_path(self) -> str:
        """Obtiene la ruta completa de la categoría (ej: Electrónica > Celulares)"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name