"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# ----------------------
# Core HMS Schemas
# ----------------------

class Patient(BaseModel):
    full_name: str = Field(..., description="Patient full name")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    gender: Optional[Literal["Male", "Female", "Other"]] = Field(None, description="Gender")
    phone: Optional[str] = Field(None, description="Contact phone number")
    address: Optional[str] = Field(None, description="Home address")
    medical_history: Optional[str] = Field(None, description="Past medical history / notes")

class Doctor(BaseModel):
    full_name: str = Field(..., description="Doctor full name")
    specialization: Optional[str] = Field(None, description="Specialization/Department")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[EmailStr] = Field(None, description="Professional email")

class Appointment(BaseModel):
    patient_id: str = Field(..., description="Linked patient ID")
    doctor_id: str = Field(..., description="Linked doctor ID")
    date_time: datetime = Field(..., description="Appointment date and time (ISO)")
    reason: Optional[str] = Field(None, description="Reason / symptoms")
    status: Literal["Scheduled", "Completed", "Cancelled"] = Field("Scheduled", description="Appointment status")

# Example schemas kept for reference (not used by app directly)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
