from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticketSchema import TicketCreate
from datetime import datetime

def create_ticket(db: Session, ticket: TicketCreate):
    db_ticket = Ticket(**ticket.dict(), booking_time=datetime.utcnow())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

# Thống kê vé theo phim
def stats_tickets_by_movie(db: Session):
    return db.query(
        Ticket.showtime_id,
        func.count(Ticket.ticket_id).label("total_tickets")
    ).group_by(Ticket.showtime_id).all()

# Thống kê vé theo ngày
def stats_tickets_by_date(db: Session):
    return db.query(
        func.date(Ticket.booking_time).label("date"),
        func.count(Ticket.ticket_id).label("total_tickets")
    ).group_by(func.date(Ticket.booking_time)).all()
