from fastapi import FastAPI
from routes import movies

app = FastAPI(title="Movie Booking API")

app.include_router(movies.router, prefix="/movies", tags=["Movies"])

@app.get("/")
def root():
    return {"message": "Welcome to Movie Booking API"}
