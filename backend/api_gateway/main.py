import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from loguru import logger

app = FastAPI(title="Remedic Connect API Gateway")

SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "patient": os.getenv("PATIENT_SERVICE_URL", "http://localhost:8002"),
    "lab": os.getenv("LAB_SERVICE_URL", "http://localhost:8003"),
    "pharmacy": os.getenv("PHARMACY_SERVICE_URL", "http://localhost:8004"),
    "ai": os.getenv("AI_SERVICE_URL", "http://localhost:8005"),
    "admin": os.getenv("ADMIN_SERVICE_URL", "http://localhost:8006"),
}


@app.on_event("startup")
def on_startup() -> None:
    os.makedirs("logs", exist_ok=True)
    logger.add("logs/api_gateway.log", rotation="1 MB", retention=5)


@app.get("/health")
def health() -> dict:
    return {"service": "api_gateway", "status": "ok"}


@app.api_route("/api/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service_name: str, path: str, request: Request):
    base_url = SERVICE_MAP.get(service_name)
    if not base_url:
        raise HTTPException(status_code=404, detail="Unknown service")

    url = f"{base_url}/{service_name}/{path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.request(
                request.method,
                url,
                content=body,
                headers=headers,
                params=request.query_params,
            )
    except httpx.HTTPError as exc:
        logger.error("Gateway error service={} path={} error={}", service_name, path, str(exc))
        raise HTTPException(status_code=502, detail=f"Service unavailable: {exc}")

    try:
        content = resp.json()
    except ValueError:
        content = {"message": resp.text}

    return JSONResponse(status_code=resp.status_code, content=content)
