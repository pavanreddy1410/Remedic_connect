from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/patient", tags=["patient"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "patient_service",
        "message": "Starter endpoint for patient_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8002,
    }
