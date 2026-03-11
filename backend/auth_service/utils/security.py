from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt



def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")



def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))



def create_access_token(payload: dict, secret_key: str, algorithm: str, expires_minutes: int) -> str:
    data = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, secret_key, algorithm=algorithm)



def decode_token(token: str, secret_key: str, algorithm: str) -> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
