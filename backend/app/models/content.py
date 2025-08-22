from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.database import Base

class Content(Base):
    __tablename__ = "contents"

    content_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text)
    type = Column(String, nullable=False)  # news / promotion / announcement
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
