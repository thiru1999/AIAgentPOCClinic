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

@app.get("/check_availability")
def check_availability(date: str, time: str):
    """Checks if a slot is available (mock logic)."""
    # Mock Logic: All slots in future are available for POC
    return {"available": True, "message": f"Slot at {time} on {date} is available."}

@app.post("/book_appointment")
def book_appointment(appointment: Appointment):
    """Books an appointment and notifies the dashboard."""
    logger.info(f"Booking received: {appointment}")
    
    # Enrich with timestamp
    appointment.booked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    appointments_db.insert(0, appointment) # Add to top of list
    
    return {"status": "success", "booking_id": f"bk_{len(appointments_db)}", "message": "Booking Confirmed"}

# --- Technician Dashboard Endpoints ---

@app.get("/appointments")
def get_appointments():
    """Returns all booked appointments for the dashboard."""
    return appointments_db
