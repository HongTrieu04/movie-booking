from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShowtimeBase(BaseModel):
    movie_id: int
    cinema_id: int
    screen_id: Optional[int] = None
    start_time: datetime
    price: float

class ShowtimeCreate(ShowtimeBase):
    pass

class ShowtimeUpdate(BaseModel):
    start_time: Optional[datetime] = None
    price: Optional[float] = None
    screen_id: Optional[int] = None

class ShowtimeResponse(ShowtimeBase):
    showtime_id: int

    class Config:
        from_attributes = True

