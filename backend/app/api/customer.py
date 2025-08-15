from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.userSchema import UserLogin, UserCreate, UserResponse 
from app.db.database import depend_db
from app.core.auth import authenticate_user, create_access_token
from app.services import userService

roleCustomer = "customer"
routeCustomer = APIRouter(prefix="/customer", tags=["Customer"])

@routeCustomer.post("/register",response_model=UserResponse)
def Register(newUser: UserCreate, db: Session = Depends(depend_db)):
    if userService.checkExist(db, newUser.phone, newUser.email):
        raise HTTPException(status_code=409, detail="Phone or email already exists")
    return userService.create_user(db, newUser, roleUser=roleCustomer)
@routeCustomer.post("/login")
def Login(user: UserLogin, db: Session = Depends(depend_db)):
    userCheck = authenticate_user(user.phone, user.password, db)
    if not userCheck or userCheck.role != roleCustomer:
        raise HTTPException(status_code=401, detail="Login failed")
    token = create_access_token(data={"sub": user.phone})
    return {"access_token": token}