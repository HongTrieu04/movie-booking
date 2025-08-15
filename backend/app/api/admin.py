from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.userSchema import UserCreate, UserResponse ,UserLogin
from app.db.database import depend_db
from app.services import userService
from app.core.auth import authenticate_user,create_access_token,requireAdmin

roleAdmin="admin"
routeAdmin = APIRouter(prefix="/admin", tags=["Admin"])

@routeAdmin.post("/register",response_model=UserResponse)
def createAdmin(newUser:UserCreate,db:Session=Depends(depend_db),user: User = Depends(requireAdmin)):
    if userService.checkExist(db,newUser.phone,newUser.email):
        raise HTTPException(status_code=409, detail="Phone or email already exists")
    return userService.create_user(db, newUser,roleUser=roleAdmin)
@routeAdmin.post("/login")
def Login(user : UserLogin, db:Session=Depends(depend_db)):
    userCheck = authenticate_user(user.phone,user.password,db)
    if not userCheck or userCheck.role != roleAdmin:
        raise HTTPException(status_code=401, detail="Login failed")
    token = create_access_token(data={"sub": user.phone})
    return {"access_token: ": token}
@routeAdmin.delete("/delete")
def deleteUser(user_id: int, db: Session = Depends(depend_db), user: User = Depends(requireAdmin)):
    return userService.delete_user(db,user_id)
@routeAdmin.get("/getUser/{user_id}", response_model=UserResponse)
def getUser(user_id:int,db:Session=Depends(depend_db),user: User = Depends(requireAdmin)):
    userGet = userService.get_user_by_id(db, user_id)
    if not userGet:
        raise HTTPException(status_code=404, detail="User not found")
    return userGet
@routeAdmin.get("/getAllUsers",response_model=list[UserResponse])
def getAllUsers(skip: int = 0, limit: int = 100, db: Session = Depends(depend_db), user: User = Depends(requireAdmin)):
    users = userService.get_all_users(db, skip=skip, limit=limit)
    return users