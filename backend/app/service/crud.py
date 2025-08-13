from sqlalchemy.orm import Session
from schemas.adminSche import Admin
from models.accModel import User
def createAdmin(ad: Admin, db: Session):
    admin=db.query(User).filter(User.name == ad.name).first()
    if admin is not None:
        return {"message": "Admin already exists"}
    else:
        newuser=User(name=ad.name,password=ad.password,role="admin",email=ad.email,phone_number=ad.phone_number)
        db.add(newuser)
        db.commit()
    return {"message": "Admin created successfully"}

