from sqlalchemy import Column, Integer, String, CheckConstraint
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="customer", nullable=False)
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete")

    __table_args__ = (
        CheckConstraint("role IN ('customer', 'admin')", name="check_role"),
    )
