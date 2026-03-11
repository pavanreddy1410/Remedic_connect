from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from loguru import logger

from services.db import db
from models.schemas import ApprovalRequest
from utils.auth import require_roles
from utils.rate_limit import limiter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def list_users(_: dict = Depends(require_roles("admin"))):
    users = []
    for user in db.users.find({}, {"password": 0}):
        user["id"] = str(user.pop("_id"))
        users.append(user)
    return users


@router.post("/approve/{target_role}")
@limiter.limit("5/second")
def approve_entity(target_role: str, request: Request, payload: ApprovalRequest, user: dict = Depends(require_roles("admin"))):
    db.audit_logs.insert_one(
        {
            "action": f"approve_{target_role}",
            "admin_id": user["sub"],
            "user_id": payload.user_id,
            "approved": payload.approved,
            "created_at": datetime.now(timezone.utc),
        }
    )
    logger.info("Admin approval admin_id={} target_role={} user_id={} approved={}", user["sub"], target_role, payload.user_id, payload.approved)
    return {"message": f"{target_role} approval recorded"}


@router.get("/audit-logs")
def get_audit_logs(_: dict = Depends(require_roles("admin"))):
    logs = []
    for item in db.audit_logs.find().sort("created_at", -1).limit(100):
        item["id"] = str(item.pop("_id"))
        logs.append(item)
    return logs
