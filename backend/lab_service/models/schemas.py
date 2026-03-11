from datetime import datetime
from pydantic import BaseModel


class LabReportCreate(BaseModel):
    patient_id: str
    test_type: str
    verification_status: str = "verified"


class LabReportOut(BaseModel):
    id: str
    patient_id: str
    lab_id: str
    test_type: str
    report_url: str
    verification_status: str
    created_at: datetime
