from sqlalchemy import Column, Integer, String, Text, Date, Boolean, Numeric, CheckConstraint
from app.db.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    promo_id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    description = Column(Text)
    discount_type = Column(String, nullable=False)  # percentage / fixed
    discount_value = Column(Numeric(10,2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("discount_type IN ('percentage','fixed')", name="check_discount_type"),
    )
