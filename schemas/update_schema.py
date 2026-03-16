from pydantic import BaseModel

class DoctorUpdate(BaseModel):
    full_name: str
    designation: str
    department: str
    email: str
    contact_number: str
    hospital: str
    facility_type: str
    address: str
    city: str
    state: str
    pin: int
    license: str
    certificate: str
    proof: str
    country: str