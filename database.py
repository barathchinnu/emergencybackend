from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Update with your MySQL credentials
# In production (Render), DATABASE_URL will be provided by environment variables
raw_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:barath%402007@localhost:3306/medical_response_db")

# Debug logging for Render (password hidden)
if "@" in raw_url:
    masked_url = raw_url.split("@")[-1]
    print(f"DEBUG: Connecting to database at ...@{masked_url}")
else:
    print(f"DEBUG: Connecting to database URL: {raw_url}")

# Ensure we aren't accidentally using an https URL from another setting
if raw_url.startswith("https"):
    print("CRITICAL ERROR: DATABASE_URL starts with 'https'. Please check your Render environment variables!")
    # Fallback to local if it's clearly wrong, or keep it to let SQLAlchemy throw the clear error
    SQLALCHEMY_DATABASE_URL = raw_url
else:
    SQLALCHEMY_DATABASE_URL = raw_url
    # For Railway/Render, we might need to handle the 'mysql://' vs 'mysql+pymysql://' prefix
    if SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    
    # Fix 'ssl-mode' (hyphen) to 'ssl_mode' (underscore) for PyMySQL compatibility
    if "ssl-mode=" in SQLALCHEMY_DATABASE_URL:
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("ssl-mode=", "ssl_mode=")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
