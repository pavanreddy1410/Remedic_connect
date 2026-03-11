from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/info")
def service_info() -> dict:
    return {
        "service": "ai_service",
        "message": "Starter endpoint for ai_service",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port": 8005,
    }
