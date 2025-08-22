from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.contentSchema import ContentCreate, ContentUpdate, ContentResponse
from app.services import content as content_service
from typing import List

router = APIRouter(prefix="/contents", tags=["Contents"])

@router.post("/", response_model=ContentResponse)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    return content_service.create_content(db, content)

@router.get("/", response_model=List[ContentResponse])
def list_contents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return content_service.get_contents(db, skip=skip, limit=limit)

@router.get("/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    db_content = content_service.get_content(db, content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.put("/{content_id}", response_model=ContentResponse)
def update_content(content_id: int, updates: ContentUpdate, db: Session = Depends(get_db)):
    db_content = content_service.update_content(db, content_id, updates)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.delete("/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_content = content_service.delete_content(db, content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}
