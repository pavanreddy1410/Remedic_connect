from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "auth_service",
        "message": "Starter endpoint for auth_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8001,
    }
