from sqlalchemy.orm import Session
from models.doctor_model import Doctor
from schemas.doctor_schema import DoctorCreate
from fastapi import HTTPException
from auth.password_handler import get_password_hash
from blockchain.blockservice import add_block, verify_chain


def register_doctor(db: Session, doctor: DoctorCreate):

    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Doctor already exists")

    if doctor.password != doctor.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hash_password = get_password_hash(doctor.password)

    new_doctor = Doctor(
        full_name=doctor.full_name,
        designation=doctor.designation,
        department=doctor.department,
        email=doctor.email,
        contact_number=doctor.contact_number,
        hospital=doctor.hospital,
        facility_type=doctor.facility_type,
        address=doctor.address,
        city=doctor.city,
        state=doctor.state,
        pin=doctor.pin,
        license=doctor.license,
        certificate=doctor.certificate,
        proof=doctor.proof,
        country=doctor.country,
        password=hash_password
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    data = {
        "id": new_doctor.id,
        "email": new_doctor.email,
        "contact": new_doctor.contact_number,
        "license": new_doctor.license
    }

    add_block(db, new_doctor.id, "doctors", data)

    return new_doctor


def get_all_records(db: Session):

    doctors = db.query(Doctor).all()

    if not doctors:
        raise HTTPException(status_code=404, detail="No records found")

    return doctors


def update_doctor(db: Session, doctor_id: int, doctor_data):

    # Update se pehle chain verify karo
    chain_status = verify_chain(db)
    if not chain_status["valid"]:
        raise HTTPException(
            status_code=409,
            detail=f"Blockchain integrity compromised: {chain_status['reason']}"
        )

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.full_name = doctor_data.full_name
    doctor.designation = doctor_data.designation
    doctor.department = doctor_data.department
    doctor.contact_number = doctor_data.contact_number
    doctor.hospital = doctor_data.hospital
    doctor.facility_type = doctor_data.facility_type
    doctor.address = doctor_data.address
    doctor.city = doctor_data.city
    doctor.state = doctor_data.state
    doctor.pin = doctor_data.pin
    doctor.license = doctor_data.license
    doctor.certificate = doctor_data.certificate
    doctor.proof = doctor_data.proof
    doctor.country = doctor_data.country

    db.commit()
    db.refresh(doctor)

    data = {
        "id": doctor.id,
        "email": doctor.email,
        "contact": doctor.contact_number,
        "license": doctor.license
    }

    add_block(db, doctor.id, "doctors", data)

    return doctor


def remove_records(db:Session, doctor_id:int):
    
    chain_status = verify_chain(db)
    
    if not chain_status["valid"]:
        raise HTTPException(
            status_code=409,
            detail=f"Blockchain integrity compromised: {chain_status['reason']}"
        )
        
        
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    if not doctor :
        raise HTTPException(status_code=404, detail= "doctor not found ")
    
    
    data = {
        "id": doctor.id,
        "email": doctor.email,
        "contact": doctor.contact_number,
        "license": doctor.license
    }
    
    add_block(db,doctor_id,"doctors",data)
    
    db.delete(doctor)
    db.commit()
    
    return {"message" : "doctor details deleted successfully "}