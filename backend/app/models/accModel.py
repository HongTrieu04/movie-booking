from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from db.database import Base

class User(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(15), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20)) 
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

