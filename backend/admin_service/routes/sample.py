from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "admin_service",
        "message": "Starter endpoint for admin_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8006,
    }
