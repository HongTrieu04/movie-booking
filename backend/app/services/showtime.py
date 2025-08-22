from sqlalchemy.orm import Session
from app.models.showtime import Showtime
from app.schemas.showtimeSchema import ShowtimeCreate, ShowtimeUpdate

def create_showtime(db: Session, showtime: ShowtimeCreate):
    db_showtime = Showtime(**showtime.dict())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

def update_showtime(db: Session, showtime_id: int, updates: ShowtimeUpdate):
    db_showtime = db.query(Showtime).filter(Showtime.showtime_id == showtime_id).first()
    if not db_showtime:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_showtime, key, value)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime

def delete_showtime(db: Session, showtime_id: int):
    db_showtime = db.query(Showtime).filter(Showtime.showtime_id == showtime_id).first()
    if not db_showtime:
        return None
    db.delete(db_showtime)
    db.commit()
    return db_showtime

def get_showtimes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Showtime).offset(skip).limit(limit).all()

def get_showtime(db: Session, showtime_id: int):
    return db.query(Showtime).filter(Showtime.showtime_id == showtime_id).first()
