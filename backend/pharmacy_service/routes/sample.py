from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/pharmacy", tags=["pharmacy"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "pharmacy_service",
        "message": "Starter endpoint for pharmacy_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8004,
    }
