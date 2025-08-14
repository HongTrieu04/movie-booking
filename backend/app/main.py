from fastapi import FastAPI
from .routes.user import router as user_router
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)  
app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Welcome to my app"}

app.include_router(user_router)
