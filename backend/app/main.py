from fastapi import FastAPI
from api.admin import routeAdmin
from db.database import engine, Base

Base.metadata.create_all(bind=engine)  
app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Welcome to my app"}

app.include_router(routeAdmin)