from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContentBase(BaseModel):
    title: str
    body: Optional[str] = None
    type: str  # news, promotion, announcement

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    type: Optional[str] = None

class ContentResponse(ContentBase):
    content_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

