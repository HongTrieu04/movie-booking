from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.movieSchema import MovieCreate, MovieUpdate, MovieResponse
from app.services import movie as movie_service
from typing import List

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(db, movie)

@router.get("/", response_model=List[MovieResponse])
def list_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return movie_service.get_movies(db, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = movie_service.get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, updates: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = movie_service.update_movie(db, movie_id, updates)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = movie_service.delete_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}
