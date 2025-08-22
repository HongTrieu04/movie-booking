from pydantic import BaseModel
from datetime import date
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[date] = None
    language: Optional[str] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    rating: Optional[str] = None
    status: Optional[str] = "coming_soon"

class MovieCreate(MovieBase):
    title: str  # bắt buộc khi tạo mới

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    release_date: Optional[date] = None
    language: Optional[str] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    rating: Optional[str] = None
    status: Optional[str] = None

class MovieResponse(MovieBase):
    movie_id: int

    class Config:
        from_attributes = True

