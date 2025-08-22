from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.services import user as user_service
from app.schemas.userSchema import UserCreate
import requests
from jose import jwt, JWTError

def exchange_code_for_tokens(code: str):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    resp = requests.post(settings.GOOGLE_TOKEN_URL, data=data)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get token from Google")
    return resp.json()

def verify_google_token(id_token: str):
    jwks = requests.get(settings.GOOGLE_JWKS_URL).json()
    unverified_header = jwt.get_unverified_header(id_token)

    key = next((jwk for jwk in jwks["keys"] if jwk["kid"] == unverified_header["kid"]), None)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    try:
        payload = jwt.decode(
            id_token,
            key,
            algorithms=["RS256"],
            audience=settings.GOOGLE_CLIENT_ID,
            issuer=["https://accounts.google.com", "accounts.google.com"],
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

def login_with_google(db: Session, code: str):
    tokens = exchange_code_for_tokens(code)
    id_token = tokens["id_token"]
    google_user = verify_google_token(id_token)

    email = google_user["email"]
    name = google_user.get("name", email.split("@")[0])

    # Tìm user trong DB
    user = user_service.get_user_by_email(db, email)
    if not user:
        user = user_service.create_user(db, UserCreate(
            name=name,
            email=email,
            phone=None,
            password=None,  # Google user không cần password
            role="customer"
        ))

    # Chuẩn hóa payload giống local login
    payload = {
        "sub": str(user.user_id),
        "preferred_username": user.name,
        "email": user.email,
        "role": user.role,
        "realm_access": {"roles": [user.role]}
    }
    access_token = create_access_token(data=payload)
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
