from sqlalchemy.orm import Session
from app.models.content import Content
from app.schemas.contentSchema import ContentCreate, ContentUpdate

def create_content(db: Session, content: ContentCreate):
    db_content = Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def update_content(db: Session, content_id: int, updates: ContentUpdate):
    db_content = db.query(Content).filter(Content.content_id == content_id).first()
    if not db_content:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_content, key, value)
    db.commit()
    db.refresh(db_content)
    return db_content

def delete_content(db: Session, content_id: int):
    db_content = db.query(Content).filter(Content.content_id == content_id).first()
    if not db_content:
        return None
    db.delete(db_content)
    db.commit()
    return db_content

def get_contents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Content).offset(skip).limit(limit).all()

def get_content(db: Session, content_id: int):
    return db.query(Content).filter(Content.content_id == content_id).first()
