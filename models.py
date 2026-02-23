from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False)

class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(200))

class EmergencyRequest(Base):
    __tablename__ = "emergency_request"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50), name="user_id")
    latitude = Column(Float)
    longitude = Column(Float)
    assignedAmbulanceId = Column(String(50), name="assigned_ambulance_id")
    status = Column(String(20)) # e.g., PENDING, COMPLETED
    natureOfEmergency = Column(String(100), name="nature_of_emergency")
    hospitalId = Column(Integer, name="hospital_id")
    hospitalStatus = Column(String(20), name="hospital_status") # PENDING, ACCEPTED
    doctorName = Column(String(100), name="doctor_name")
