import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os

OIDC_ISSUER = os.getenv("OIDC_ISSUER", "http://localhost:8080/auth/realms/movie")
OIDC_AUDIENCE = os.getenv("OIDC_API_AUDIENCE", "movie-api")
OIDC_JWKS_URL = f"{OIDC_ISSUER}/protocol/openid-connect/certs"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cache JWKS
_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        resp = requests.get(OIDC_JWKS_URL)
        resp.raise_for_status()
        _jwks_cache = resp.json()
    return _jwks_cache

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)

        key = None
        for jwk in jwks["keys"]:
            if jwk["kid"] == unverified_header["kid"]:
                key = jwk
                break

        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token: key not found")

        payload = jwt.decode(
            token,
            key,
            algorithms=[key["alg"]],
            audience=OIDC_AUDIENCE,
            issuer=OIDC_ISSUER,
        )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
