from sqlalchemy import Column, Integer, String, DateTime ,ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    blood_type = Column(String(5), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    plan_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    requestor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_name = Column(String(100), nullable=False)
    blood_type = Column(String(5), nullable=False)
    request_type = Column(String(20), nullable=False, default="patient-specific")
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.now)