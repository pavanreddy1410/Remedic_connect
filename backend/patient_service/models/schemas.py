from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class MedicineOrder(BaseModel):
    pharmacy_id: str
    medicines: List[str] = Field(min_items=1)


class ShareReportRequest(BaseModel):
    report_id: str
    doctor_id: str


class OrderResponse(BaseModel):
    id: str
    status: str
    created_at: datetime
