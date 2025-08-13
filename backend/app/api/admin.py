from fastapi import APIRouter, Depends
from requests import Session

from schemas.adminSche import Admin
from service import crud
from db.database import depend_db

routeAdmin = APIRouter(prefix="/admin", tags=["Admin"])

@routeAdmin.post("/")
def create_admin(admin: Admin, db: Session = Depends(depend_db)):
    return crud.createAdmin(admin, db)

