from pydantic import BaseModel
from datetime import date
from typing import Optional

class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str  # percentage / fixed
    discount_value: float
    start_date: date
    end_date: date
    quantity: int
    is_active: Optional[bool] = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None

class PromotionResponse(PromotionBase):
    promo_id: int

    class Config:
        from_attributes = True

