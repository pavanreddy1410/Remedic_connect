import os
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from loguru import logger
from utils.rate_limit import limiter
from routes.health import router as health_router
from routes.auth import router as auth_router
from services.db import ensure_indexes


app = FastAPI(title="Remedic Connect Auth Service")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.include_router(health_router)
app.include_router(auth_router)


@app.on_event("startup")
def on_startup() -> None:
    os.makedirs("logs", exist_ok=True)
    logger.add("logs/auth_service.log", rotation="1 MB", retention=5)
    ensure_indexes()
