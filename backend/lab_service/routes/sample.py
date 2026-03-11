from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/lab", tags=["lab"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "lab_service",
        "message": "Starter endpoint for lab_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8003,
    }
