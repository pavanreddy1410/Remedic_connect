from pydantic import BaseModel, Field
from typing import Dict, List


class InteractionRequest(BaseModel):
    medicines: List[str] = Field(min_items=2)


class LabMetrics(BaseModel):
    glucose: float | None = None
    cholesterol: float | None = None
    hemoglobin: float | None = None
