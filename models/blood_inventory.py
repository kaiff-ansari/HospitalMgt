from sqlalchemy import Column, Integer, String, Date, Text
from datetime import date
from models.doctor_model import Base


class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id = Column(Integer, primary_key=True, index=True)

    blood_group = Column(String(5), nullable=False)
    
    rh_factor = Column(String(3), nullable=False)
    
    expire_date = Column(Date, nullable=False)

    status = Column(String(20), default="available")

    notes = Column(Text, nullable=True)