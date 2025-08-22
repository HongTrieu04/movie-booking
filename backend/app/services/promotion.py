from sqlalchemy.orm import Session
from app.models.promotion import Promotion
from app.schemas.promotionSchema import PromotionCreate, PromotionUpdate

def create_promotion(db: Session, promotion: PromotionCreate):
    db_promo = Promotion(**promotion.dict())
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return db_promo

def update_promotion(db: Session, promo_id: int, updates: PromotionUpdate):
    db_promo = db.query(Promotion).filter(Promotion.promo_id == promo_id).first()
    if not db_promo:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_promo, key, value)
    db.commit()
    db.refresh(db_promo)
    return db_promo

def delete_promotion(db: Session, promo_id: int):
    db_promo = db.query(Promotion).filter(Promotion.promo_id == promo_id).first()
    if not db_promo:
        return None
    db.delete(db_promo)
    db.commit()
    return db_promo

def get_promotions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Promotion).offset(skip).limit(limit).all()

def get_promotion_by_code(db: Session, code: str):
    return db.query(Promotion).filter(Promotion.code == code, Promotion.is_active == True).first()
