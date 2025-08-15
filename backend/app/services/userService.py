from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.userSchema import UserCreate, UserUpdate,UserGet
from app.core.auth import get_password_hash


def create_user(db: Session, user: UserCreate,roleUser:str):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        role=roleUser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    users= db.query(User).offset(skip).limit(limit).all()
    return users
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.phone is not None:
        db_user.phone = user_update.phone
    if user_update.password is not None:
        db_user.password_hash = get_password_hash(user_update.password)
    if user_update.role is not None:
        db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
def checkExist(db:Session,phone:str,email:str):
    user=db.query(User).with_entities(User.phone,User.email).filter((User.phone==phone) or (User.email==email)).first()
    if user:
        return True
    return False