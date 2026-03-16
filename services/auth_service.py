from sqlalchemy.orm import Session
from schemas.auth_schema import LoginRequest
from models.doctor_model import Doctor
from fastapi import HTTPException,Request
from auth.password_handler import verify_password
from auth.jwt_handler import create_access_token,SECRET_KEY,ALGORITHM
import jwt



def log_in(db: Session, email: str, password: str):

    doctor = db.query(Doctor).filter(Doctor.email == email).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not verify_password(password, doctor.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    token = create_access_token({
        "doctor_id": doctor.id,
        "email": doctor.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
def is_authenticated(request: Request, db: Session):

    try:

        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=401, detail="You are unauthorized")

        token = token.split(" ")[-1]

        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        doctor_id = data.get("doctor_id")

        user = db.query(Doctor).filter(Doctor.id == doctor_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="You are unauthorized")

        return user

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")