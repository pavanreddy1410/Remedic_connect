from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import DuplicateKeyError
from loguru import logger

from config.settings import settings
from models.schemas import UserCreate, UserLogin, UserPublic, TokenResponse
from services.db import db
from utils.security import hash_password, verify_password, create_access_token
from utils.rate_limit import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/second")
def register(request: Request, payload: UserCreate):
    doc = {
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
        "role": payload.role,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        inserted = db.users.insert_one(doc)
    except DuplicateKeyError:
        logger.warning("Register failed duplicate email={}", payload.email)
        raise HTTPException(status_code=409, detail="Email already exists")

    logger.info("User registered email={} role={}", payload.email, payload.role)
    return UserPublic(
        id=str(inserted.inserted_id),
        name=doc["name"],
        email=doc["email"],
        role=doc["role"],
        created_at=doc["created_at"],
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/second")
def login(request: Request, payload: UserLogin):
    user = db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        logger.warning("Invalid login attempt email={}", payload.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "name": user["name"],
        },
        settings.secret_key,
        settings.algorithm,
        settings.access_token_expire_minutes,
    )
    logger.info("User login success email={} role={}", user["email"], user["role"])
    return TokenResponse(access_token=token)
