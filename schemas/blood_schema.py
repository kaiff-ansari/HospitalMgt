from pydantic import BaseModel
from datetime import date


class BloodInventoryCreate(BaseModel):
    blood_group: str
    rh_factor: str 
    expire_date: date
    status: str
    notes:str 
