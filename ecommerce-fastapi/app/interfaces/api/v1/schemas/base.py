from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IDSchema(BaseModel):
    id: int

class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None