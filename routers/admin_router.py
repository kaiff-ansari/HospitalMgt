from fastapi import APIRouter,Depends
from database.connection import get_db
from sqlalchemy.orm import Session
from services import admin_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login")
def add_admin(form_data : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    return admin_service.admin_login(db,form_data.username, form_data.password)