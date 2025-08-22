from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint
from app.db.database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration = Column(Integer)
    release_date = Column(Date)
    language = Column(String)
    genre = Column(String)
    poster_url = Column(String)
    trailer_url = Column(String)
    rating = Column(String)
    status = Column(String, default="coming_soon")  # now_showing, coming_soon, stopped

    __table_args__ = (
        CheckConstraint("status IN ('now_showing','coming_soon','stopped')", name="check_movie_status"),
    )
