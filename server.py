import json
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diagnostic Clinic POC API")

# Allow CORS for the Technician Dashboard (Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Appointment(BaseModel):
    patient_name: str
    age: Optional[str] = None
    contact_number: Optional[str] = None
    scan_type: str
    appointment_date: str
    appointment_time: str
    status: str = "Pending"
    booked_at: str = datetime.now().isoformat()

# --- Load Knowledge Base ---
def load_data():
    with open("knowledge_base.json", "r") as f:
        return json.load(f)

# In-memory storage for appointments (for POC)
appointments_db: List[Appointment] = []

@app.get("/")
def read_root():
    return {"status": "System Operational", "service": "Diagnostic Clinic AI Backend"}

# --- Vapi.ai Tool Endpoints ---

@app.get("/services")
def get_services():
    """Returns list of available scans and prices."""
    data = load_data()
    return {"scans": data["scans"]}

@app.post("/check_availability")
def check_availability(payload: dict = {}):
    return {
        "available": True,
        "message": "Yes madam, slot available. Book pannalama?"
    }

@app.post("/book_appointment")
def book_appointment(payload: dict):
    dummy_record = {
        "patient_name": payload.get("patient_name", "Workflow Test"),
        "scan_type": payload.get("scan_type", "MRI"),
        "appointment_date": payload.get("date", "today"),
        "appointment_time": payload.get("time", "any time"),
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    appointments_db.insert(0, dummy_record)

    return {
        "status": "success",
        "message": "Booking done"
    }

# --- Technician Dashboard Endpoints ---

@app.get("/appointments")
def get_appointments():
    """Returns all booked appointments for the dashboard."""
    return appointments_db


