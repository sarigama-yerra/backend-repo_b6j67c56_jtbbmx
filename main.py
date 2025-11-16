import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import datetime

from schemas import Patient, Doctor, Appointment
from database import create_document, get_documents, db

app = FastAPI(title="Nilkanth Medico HMS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Nilkanth Medico Private Limited - HMS Backend Running"}

@app.get("/company")
def company_info():
    return {
        "name": "Nilkanth Medico Private Limited",
        "product": "Hospital Management Software",
        "version": "1.0.0"
    }

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ----------------------
# Patients
# ----------------------
@app.post("/api/patients")
def create_patient(payload: Patient):
    try:
        inserted_id = create_document("patient", payload)
        return {"inserted_id": inserted_id, "message": "Patient created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patients")
def list_patients(limit: Optional[int] = Query(default=100, ge=1, le=1000)):
    try:
        docs = get_documents("patient", limit=limit)
        # Convert ObjectId to str
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"]) 
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# Doctors
# ----------------------
@app.post("/api/doctors")
def create_doctor(payload: Doctor):
    try:
        inserted_id = create_document("doctor", payload)
        return {"inserted_id": inserted_id, "message": "Doctor created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/doctors")
def list_doctors(limit: Optional[int] = Query(default=100, ge=1, le=1000)):
    try:
        docs = get_documents("doctor", limit=limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"]) 
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# Appointments
# ----------------------
@app.post("/api/appointments")
def create_appointment(payload: Appointment):
    try:
        inserted_id = create_document("appointment", payload)
        return {"inserted_id": inserted_id, "message": "Appointment created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/appointments")
def list_appointments(
    limit: Optional[int] = Query(default=100, ge=1, le=1000),
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
):
    try:
        filter_dict = {}
        if patient_id:
            filter_dict["patient_id"] = patient_id
        if doctor_id:
            filter_dict["doctor_id"] = doctor_id
        if status:
            filter_dict["status"] = status
        docs = get_documents("appointment", filter_dict=filter_dict, limit=limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"]) 
            # Convert datetime to isoformat for JSON
            if "date_time" in d and isinstance(d["date_time"], datetime):
                d["date_time"] = d["date_time"].isoformat()
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
