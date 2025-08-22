from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.promotionSchema import PromotionCreate, PromotionUpdate, PromotionResponse
from app.services import promotion as promo_service

router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.post("/", response_model=PromotionResponse)
def create_promo(promo: PromotionCreate, db: Session = Depends(get_db)):
    return promo_service.create_promotion(db, promo)

@router.get("/", response_model=List[PromotionResponse])
def list_promotions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return promo_service.get_promotions(db, skip=skip, limit=limit)

@router.put("/{promo_id}", response_model=PromotionResponse)
def update_promo(promo_id: int, updates: PromotionUpdate, db: Session = Depends(get_db)):
    db_promo = promo_service.update_promotion(db, promo_id, updates)
    if not db_promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return db_promo

@router.delete("/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    db_promo = promo_service.delete_promotion(db, promo_id)
    if not db_promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return {"message": "Promotion deleted successfully"}
