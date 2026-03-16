from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.doctor_schema import DoctorCreate
from schemas.update_schema import DoctorUpdate
from services import doctor_service
from auth.ouath2 import get_current_user

router = APIRouter()

@router.post("/doctor/register")
def register_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.register_doctor(db, doctor)


@router.get("/doctor")
def get_all_records(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    return doctor_service.get_all_records(db)


@router.put("/update/{doctor_id}")
def update_record(doctor_id:int, doctor_data:DoctorUpdate, db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return doctor_service.update_doctor(db, doctor_id, doctor_data)


@router.delete("/doctor/{doctor_id}")
def delete_details(doctor_id:int, db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return doctor_service.remove_records(db,doctor_id)