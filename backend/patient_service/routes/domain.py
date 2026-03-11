from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from loguru import logger

from services.db import db
from models.schemas import MedicineOrder, ShareReportRequest
from utils.auth import require_roles
from utils.rate_limit import limiter

router = APIRouter(prefix="/patient", tags=["patient"])


@router.get("/reports")
def my_reports(user: dict = Depends(require_roles("patient", "doctor", "admin"))):
    query = {"patient_id": user.get("sub")} if user.get("role") == "patient" else {}
    reports = []
    for r in db.reports.find(query):
        r["id"] = str(r.pop("_id"))
        reports.append(r)
    return reports


@router.post("/orders")
@limiter.limit("5/second")
def create_order(request: Request, payload: MedicineOrder, user: dict = Depends(require_roles("patient"))):
    doc = {
        "patient_id": user["sub"],
        "pharmacy_id": payload.pharmacy_id,
        "medicines": payload.medicines,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
    }
    inserted = db.orders.insert_one(doc)
    logger.info("Medicine ordered patient_id={} pharmacy_id={} items={}", user["sub"], payload.pharmacy_id, len(payload.medicines))
    return {"id": str(inserted.inserted_id), "status": doc["status"], "created_at": doc["created_at"]}


@router.post("/share-report")
def share_report(payload: ShareReportRequest, user: dict = Depends(require_roles("patient"))):
    db.audit_logs.insert_one(
        {
            "action": "share_report",
            "patient_id": user["sub"],
            "doctor_id": payload.doctor_id,
            "report_id": payload.report_id,
            "created_at": datetime.now(timezone.utc),
        }
    )
    return {"message": "Report shared successfully"}
