from pydantic import BaseModel
from datetime import datetime

class TicketBase(BaseModel):
    user_id: int
    showtime_id: int
    seat_number: str

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    ticket_id: int
    booking_time: datetime

    class Config:
        from_attributes = True

