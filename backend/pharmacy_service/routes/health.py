from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> dict:
    return {"service": "pharmacy_service", "status": "ok"}
