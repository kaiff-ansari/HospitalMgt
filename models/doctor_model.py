from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    designation = Column(String)
    department = Column(String)
    email = Column(String, unique=True, index=True)
    contact_number = Column(String)
    hospital = Column(String)
    facility_type = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    pin = Column(Integer)
    license = Column(String)
    certificate = Column(String)
    proof = Column(String)
    country = Column(String)
    password = Column(String)
    