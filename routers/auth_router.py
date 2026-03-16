from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.auth_schema import LoginRequest
from services import auth_service
from auth.ouath2 import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    email = form_data.username
    password = form_data.password

    return auth_service.log_in(db, email, password)


@router.get("/validate")
def is_authenitcated(current_user =  Depends(get_current_user)):
   
   return{
       "user":current_user.id,
       "email": current_user.email
       
   }