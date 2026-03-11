from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from loguru import logger

from services.db import db
from utils.auth import require_roles
from utils.rate_limit import limiter

router = APIRouter(prefix="/lab", tags=["lab"])
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/reports/upload")
@limiter.limit("5/second")
async def upload_report(
    request: Request,
    patient_id: str = Form(...),
    test_type: str = Form(...),
    verification_status: str = Form("verified"),
    report_file: UploadFile = File(...),
    user: dict = Depends(require_roles("lab")),
):
    suffix = Path(report_file.filename).suffix or ".bin"
    file_name = f"{uuid4().hex}{suffix}"
    destination = REPORTS_DIR / file_name

    with destination.open("wb") as f:
        f.write(await report_file.read())

    doc = {
        "patient_id": patient_id,
        "lab_id": user["sub"],
        "test_type": test_type,
        "report_url": str(destination).replace("\\", "/"),
        "verification_status": verification_status,
        "created_at": datetime.now(timezone.utc),
    }
    inserted = db.reports.insert_one(doc)
    logger.info("Report uploaded lab_id={} patient_id={} file={}", user["sub"], patient_id, destination.name)
    return {"id": str(inserted.inserted_id), **doc}


@router.get("/reports")
def list_reports(user: dict = Depends(require_roles("lab", "admin", "doctor"))):
    query = {"lab_id": user.get("sub")} if user.get("role") == "lab" else {}
    items = []
    for report in db.reports.find(query):
        report["id"] = str(report.pop("_id"))
        items.append(report)
    return items
