from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True

class HospitalBase(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class HospitalSchema(HospitalBase):
    id: int

    class Config:
        from_attributes = True

class EmergencyRequestBase(BaseModel):
    userId: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    natureOfEmergency: Optional[str] = None
    assignedAmbulanceId: Optional[str] = None
    status: Optional[str] = "PENDING"
    hospitalId: Optional[int] = None
    hospitalStatus: Optional[str] = None
    doctorName: Optional[str] = None

class EmergencyRequestCreate(EmergencyRequestBase):
    pass

class EmergencyRequestSchema(EmergencyRequestBase):
    id: int

    class Config:
        from_attributes = True
