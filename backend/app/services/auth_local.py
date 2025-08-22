from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.services.user import get_user_by_email
from app.models.user import User

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    # Chuẩn hoá payload giống Keycloak
    payload = {
        "sub": str(user.user_id),
        "preferred_username": user.name,
        "email": user.email,
        "role": user.role,
        "realm_access": {"roles": [user.role]}  # giống Keycloak
    }

    access_token = create_access_token(data=payload)
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
