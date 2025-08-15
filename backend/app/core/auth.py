from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.models.user import User
from app.db.database import depend_db


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(phone: str, password: str, db: Session):
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credential: HTTPAuthorizationCredentials = Depends(bearer_scheme),db:Session=Depends(depend_db)):
    token=credential.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.query(User).filter(User.phone == phone).first()
    if user is None:
        raise credentials_exception
    return user

def requireAdmin(user: User = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user.role != "admin":
        raise credentials_exception
    return user
def requireCustomer(user: User = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user.role != "customer":
        raise credentials_exception
    return user