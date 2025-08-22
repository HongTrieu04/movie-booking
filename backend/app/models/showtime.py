from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.orm import relationship
from app.db.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"

    showtime_id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    cinema_id = Column(Integer, ForeignKey("cinemas.cinema_id", ondelete="CASCADE"), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.screen_id", ondelete="SET NULL"))
    start_time = Column(TIMESTAMP, nullable=False)
    price = Column(Numeric(10,2), nullable=False)

    # Quan hệ ORM
    movie = relationship("Movie", backref="showtimes")
    tickets = relationship("Ticket", back_populates="showtime", cascade="all, delete")
    # có thể thêm cinema, screen nếu muốn
