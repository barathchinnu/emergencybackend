from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import engine, get_db

import os
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        logger.info("Connecting to database and creating tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # In production, we log but don't crash the server immediately
        # so that it stays up and provides logs to the user.
    
    yield
    # Shutdown logic (if any)

app = FastAPI(title="Medical Response API", lifespan=lifespan)

# Configure CORS (matching AuthController origins)
# In production, set ALLOWED_ORIGINS to your Vercel URL
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
]

if allowed_origins_env:
    origins.extend(allowed_origins_env.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Routes
@app.post("/api/auth/signup", response_model=schemas.UserSchema)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login")
def login(credentials: dict, db: Session = Depends(get_db)):
    username = credentials.get("username")
    password = credentials.get("password")
    
    user = crud.get_user_by_username(db, username=username)
    if not user or user.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return user

# Emergency Routes
@app.post("/api/emergencies", response_model=schemas.EmergencyRequestSchema)
def create_emergency(request: schemas.EmergencyRequestCreate, db: Session = Depends(get_db)):
    return crud.create_emergency_request(db=db, request=request)

@app.get("/api/emergencies", response_model=List[schemas.EmergencyRequestSchema])
def get_emergencies(db: Session = Depends(get_db)):
    return crud.get_emergency_requests(db=db)

@app.put("/api/emergencies/{id}", response_model=schemas.EmergencyRequestSchema)
def update_emergency(id: int, request_details: schemas.EmergencyRequestCreate, db: Session = Depends(get_db)):
    updated_request = crud.update_emergency_request(db, id, request_details.model_dump())
    if not updated_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated_request

# Hospital Routes
@app.get("/api/hospitals", response_model=List[schemas.HospitalSchema])
def get_hospitals(db: Session = Depends(get_db)):
    return crud.get_hospitals(db=db)

@app.post("/api/hospitals", response_model=schemas.HospitalSchema)
def create_hospital(hospital: schemas.HospitalBase, db: Session = Depends(get_db)):
    return crud.create_hospital(db=db, hospital=hospital)

@app.put("/api/hospitals/accept/{requestId}")
def accept_emergency(requestId: int, hospitalId: int, doctorName: str, db: Session = Depends(get_db)):
    updated_request = crud.accept_by_hospital(db, requestId, hospitalId, doctorName)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Emergency request not found")
    return updated_request
