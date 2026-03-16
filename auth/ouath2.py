from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.connection import get_db
from auth.password_handler import verify_access_token
from models.doctor_model import Doctor
from models.admin_model import Admin

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token:str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    
    paylaod = verify_access_token(token)
    
    if not paylaod:
        raise HTTPException(status_code=401, detail="No access Token")
    
    id = paylaod.get("doctor_id")
    user = db.query(Doctor).filter(Doctor.id == id).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Not found details ")
    
    return user


def get_admin(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="No access token")

    role = payload.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")  

    admin_id = payload.get("admin_id")
    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")  # raise add kiya

    return admin 
           
            
        
    