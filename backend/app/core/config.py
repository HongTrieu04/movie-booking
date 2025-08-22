from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Movie Booking API"
    APP_PORT: int = 8000

    # Database
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "movie_db"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"

    # Local Auth
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Keycloak / OIDC
    OIDC_ISSUER: str = "http://localhost:8080/auth/realms/movie"
    OIDC_REALM: str = "movie"
    OIDC_API_AUDIENCE: str = "movie-api"

    # Google OAuth2
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    GOOGLE_JWKS_URL: str = "https://www.googleapis.com/oauth2/v3/certs"
    GOOGLE_USERINFO_URL: str = "https://openidconnect.googleapis.com/v1/userinfo"

    class Config:
        env_file = ".env"   # load từ file .env


settings = Settings()
