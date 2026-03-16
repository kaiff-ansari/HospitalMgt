from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.blood_schema import BloodInventoryCreate
from services import blood_inventory_service
from auth.ouath2 import get_current_user

router = APIRouter(prefix="/blood")

@router.post("/add")
def add_blood_inventory(blood:BloodInventoryCreate, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
   return blood_inventory_service.add_inventory(db,blood)


@router.get("/inventory")
def get_inventory(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return blood_inventory_service.get_all_inventory(db)



@router.put("/update/{inventory_id}")
def update_inventory(inventory_id: int, blood: BloodInventoryCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return blood_inventory_service.update_blood_inventory(db, inventory_id, blood)

@router.delete("/delete/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return blood_inventory_service.delete_blood_inventory(db, inventory_id)