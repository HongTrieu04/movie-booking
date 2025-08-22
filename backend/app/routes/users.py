from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.userSchema import UserCreate, UserUpdate, UserResponse
from app.services import user as user_service
from app.db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user)

@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
