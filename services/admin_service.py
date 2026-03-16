from sqlalchemy.orm import Session
from models.admin_model import Admin
from fastapi import HTTPException
from auth.jwt_handler import create_access_token
from auth.password_handler import verify_password



def admin_login(db:Session, email:str, password:str):
    
  admin =  db.query(Admin).filter(Admin.email == email).first()
  
  if not admin:
      HTTPException(status_code=404, detail= "admin not found ")
      
  if not verify_password(password, admin.password):
      raise HTTPException(status_code=401, detail="Invalid password ")  
  
  
  token = create_access_token({
      "admin_id" : admin.id,
      "email" : admin.email,
      "password" : admin.password,
      "role" : "admin"
  })
  
  
  return {
      "access_token" : token,
      "token_type" : "bearer"
  }
    
    