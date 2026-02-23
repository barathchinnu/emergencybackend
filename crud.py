from sqlalchemy.orm import Session
import models, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password, # In real app, hash this!
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_hospitals(db: Session):
    return db.query(models.Hospital).all()

def create_hospital(db: Session, hospital: schemas.HospitalBase):
    db_hospital = models.Hospital(**hospital.model_dump())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_emergency_requests(db: Session):
    return db.query(models.EmergencyRequest).all()

def create_emergency_request(db: Session, request: schemas.EmergencyRequestCreate):
    db_data = request.model_dump()
    if not db_data.get("status"):
        db_data["status"] = "PENDING"
    db_request = models.EmergencyRequest(**db_data)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def update_emergency_request(db: Session, request_id: int, request_details: dict):
    db_request = db.query(models.EmergencyRequest).filter(models.EmergencyRequest.id == request_id).first()
    if not db_request:
        return None
    for key, value in request_details.items():
        if value is not None:
            setattr(db_request, key, value)
    db.commit()
    db.refresh(db_request)
    return db_request

def accept_by_hospital(db: Session, request_id: int, hospital_id: int, doctor_name: str):
    db_request = db.query(models.EmergencyRequest).filter(models.EmergencyRequest.id == request_id).first()
    if not db_request:
        return None
    db_request.hospitalId = hospital_id
    db_request.doctorName = doctor_name
    db_request.hospitalStatus = "ACCEPTED"
    db.commit()
    db.refresh(db_request)
    return db_request
