from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from bson import ObjectId
from loguru import logger

from services.db import db
from models.schemas import UpdateOrderStatus
from utils.auth import require_roles
from utils.rate_limit import limiter

router = APIRouter(prefix="/pharmacy", tags=["pharmacy"])


@router.get("/orders")
def pharmacy_orders(user: dict = Depends(require_roles("pharmacy", "admin"))):
    query = {"pharmacy_id": user["sub"]} if user.get("role") == "pharmacy" else {}
    items = []
    for order in db.orders.find(query):
        order["id"] = str(order.pop("_id"))
        items.append(order)
    return items


@router.patch("/orders/{order_id}")
@limiter.limit("5/second")
def update_status(order_id: str, request: Request, payload: UpdateOrderStatus, user: dict = Depends(require_roles("pharmacy"))):
    result = db.orders.update_one(
        {"_id": ObjectId(order_id), "pharmacy_id": user["sub"]},
        {"$set": {"status": payload.status, "updated_at": datetime.now(timezone.utc)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    logger.info("Order updated pharmacy_id={} order_id={} status={}", user["sub"], order_id, payload.status)
    return {"message": "Order updated", "status": payload.status}
