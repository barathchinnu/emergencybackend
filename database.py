from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Update with your MySQL credentials
# In production (Render), DATABASE_URL will be provided by environment variables
raw_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:barath%402007@localhost:3306/medical_response_db")

# Ensure we aren't accidentally using an https URL from another setting
if raw_url.startswith("https"):
    print("CRITICAL ERROR: DATABASE_URL starts with 'https'. Please check your Render environment variables!")
    SQLALCHEMY_DATABASE_URL = raw_url
else:
    SQLALCHEMY_DATABASE_URL = raw_url
    
    # 1. Handle 'mysql://' vs 'mysql+pymysql://' prefix
    if SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    
    # 2. Strip any existing ssl-mode parameters (we will handle it in connect_args)
    if "ssl-mode=" in SQLALCHEMY_DATABASE_URL:
        # Simple removal to avoid parameter conflicts
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.split("?")[0]

# Final Debug logging for Render (password hidden)
if "@" in SQLALCHEMY_DATABASE_URL:
    masked_url = SQLALCHEMY_DATABASE_URL.split("@")[-1]
    print(f"DEBUG: Final Connection URL: ...@{masked_url}")

# Production SSL settings for Aiven (bypass verify for self-signed certs)
connect_args = {}
if "aivencloud.com" in SQLALCHEMY_DATABASE_URL:
    connect_args = {
        "ssl": {
            "check_hostname": False,
            "verify_cert": False
        }
    }

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
