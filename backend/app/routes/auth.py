from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.authSchema import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services import auth_local
from app.db.database import get_db
from app.core.security import verify_any_token
from app.services import user as user_service
from app.schemas.userSchema import RegisterRequest, UserResponse, UserCreate
from app.services import user as user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    """Đăng ký tài khoản customer"""
    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Ép role = "customer"
    new_user = user_service.create_user(
        db,
        UserCreate(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=user.password,
            role="customer"
        )
    )
    return new_user

@router.post("/login-db", response_model=LoginResponse)
def login_db(login_req: LoginRequest, db: Session = Depends(get_db)):
    return auth_local.login_user(db, login_req.email, login_req.password)

@router.get("/me")
def get_me(payload: dict = Depends(verify_any_token)):
    return {
        "username": payload.get("preferred_username"),
        "email": payload.get("email"),
        "roles": payload.get("realm_access", {}).get("roles", [])
    }
