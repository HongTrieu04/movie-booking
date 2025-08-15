import os
from fastapi import FastAPI
from app.db.database import engine, Base
from .api.admin import routeAdmin
from .api.customer import routeCustomer
from sqlalchemy import text
Base.metadata.create_all(bind=engine) 
# Khi khởi tạo ứng dụng
# sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "accAdmin.sql")
# with open(sql_file_path, "r", encoding="utf-8") as f:
#     sql_statements = f.read()
# with engine.connect() as conn:
#     conn.execute(text(sql_statements))
#     conn.commit() 

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Welcome to my app"}

app.include_router(routeAdmin)
app.include_router(routeCustomer)