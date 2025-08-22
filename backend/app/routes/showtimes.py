from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.showtimeSchema import ShowtimeCreate, ShowtimeUpdate, ShowtimeResponse
from app.services import showtime as showtime_service

router = APIRouter(prefix="/showtimes", tags=["Showtimes"])

@router.post("/", response_model=ShowtimeResponse)
def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    return showtime_service.create_showtime(db, showtime)

@router.get("/", response_model=List[ShowtimeResponse])
def list_showtimes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return showtime_service.get_showtimes(db, skip=skip, limit=limit)

@router.get("/{showtime_id}", response_model=ShowtimeResponse)
def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
    db_showtime = showtime_service.get_showtime(db, showtime_id)
    if not db_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return db_showtime

@router.put("/{showtime_id}", response_model=ShowtimeResponse)
def update_showtime(showtime_id: int, updates: ShowtimeUpdate, db: Session = Depends(get_db)):
    db_showtime = showtime_service.update_showtime(db, showtime_id, updates)
    if not db_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return db_showtime

@router.delete("/{showtime_id}")
def delete_showtime(showtime_id: int, db: Session = Depends(get_db)):
    db_showtime = showtime_service.delete_showtime(db, showtime_id)
    if not db_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return {"message": "Showtime deleted successfully"}
