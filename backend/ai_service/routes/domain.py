from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from loguru import logger

from services.db import db
from models.schemas import InteractionRequest, LabMetrics
from services.analysis import detect_interactions, analyze_lab_metrics
from utils.auth import require_roles
from utils.rate_limit import limiter

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/drug-interactions")
@limiter.limit("5/second")
def drug_interactions(request: Request, payload: InteractionRequest, user: dict = Depends(require_roles("doctor", "pharmacy", "admin", "patient"))):
    findings = detect_interactions(payload.medicines)
    db.audit_logs.insert_one(
        {
            "action": "ai_drug_interaction_check",
            "requested_by": user["sub"],
            "created_at": datetime.now(timezone.utc),
        }
    )
    return {"findings": findings}


@router.post("/lab-analysis")
@limiter.limit("5/second")
def lab_analysis(request: Request, payload: LabMetrics, user: dict = Depends(require_roles("doctor", "lab", "admin", "patient"))):
    result = analyze_lab_metrics(payload.glucose, payload.cholesterol, payload.hemoglobin)
    logger.info("AI lab analysis requested by={} anomaly={}", user["sub"], result["anomaly"])
    return result
