from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.showtime_id"))
    seat_number = Column(String, nullable=False)
    booking_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tickets")
    showtime = relationship("Showtime", back_populates="tickets")
