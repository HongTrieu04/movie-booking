from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.schemas.movieSchema import MovieCreate, MovieUpdate

def create_movie(db: Session, movie: MovieCreate):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, updates: MovieUpdate):
    db_movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not db_movie:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Movie).offset(skip).limit(limit).all()

def get_movie(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.movie_id == movie_id).first()
