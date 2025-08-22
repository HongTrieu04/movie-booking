from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import ticket as ticket_crud
from app.schemas.ticketSchema import TicketCreate, TicketResponse
from typing import List

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return ticket_crud.create_ticket(db, ticket)

@router.get("/", response_model=List[TicketResponse])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ticket_crud.get_tickets(db, skip, limit)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = ticket_crud.get_ticket_by_id(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

# --- Thống kê ---
@router.get("/stats/movies")
def stats_tickets_by_movie(db: Session = Depends(get_db)):
    return ticket_crud.stats_tickets_by_movie(db)

@router.get("/stats/dates")
def stats_tickets_by_date(db: Session = Depends(get_db)):
    return ticket_crud.stats_tickets_by_date(db)
