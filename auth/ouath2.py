from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.connection import get_db
from auth.password_handler import verify_access_token
from models.doctor_model import Doctor

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
        
        
        
    