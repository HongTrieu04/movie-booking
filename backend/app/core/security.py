from datetime import datetime, timedelta
from typing import Optional
import requests
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from functools import lru_cache

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 schemas ---
oauth2_local = OAuth2PasswordBearer(tokenUrl="/auth/login-db")   # cho login DB
oauth2_oidc  = OAuth2PasswordBearer(tokenUrl="/auth/login-oidc") # giả định login qua Keycloak

# --- Password ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Token helpers ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    to_encode.update({"exp": expire, "iss": "backend", "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Dùng để đăng nhập lâu dài.
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode = data.copy()
    to_encode.update({"exp": expire, "iss": "backend", "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- JWKS cache (Keycloak) ---
@lru_cache(maxsize=1)
def get_jwks():
    return requests.get(f"{settings.OIDC_ISSUER}/protocol/openid-connect/certs").json()

# --- Verify local/oidc token ---
def verify_any_token(token: str = Depends(oauth2_local)):
    try:
        unverified = jwt.get_unverified_claims(token)
        issuer = unverified.get("iss", "")

        if issuer.startswith(settings.OIDC_ISSUER):
            # Keycloak token
            jwks = get_jwks()
            kid = jwt.get_unverified_header(token)["kid"]
            key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
            if not key:
                raise HTTPException(status_code=401, detail="Invalid Keycloak token (kid mismatch)")
            return jwt.decode(token, key, algorithms=[key["alg"]], audience=settings.OIDC_API_AUDIENCE, issuer=settings.OIDC_ISSUER)
        else:
            # Local token
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")

# --- Role-based check ---
def require_role(required_roles: list[str]):
    def role_checker(payload: dict = Depends(verify_any_token)):
        roles = payload.get("realm_access", {}).get("roles", []) or [payload.get("role")]
        if not any(role in roles for role in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return payload
    return role_checker
