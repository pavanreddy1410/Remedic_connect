from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "auth_service"
    mongo_url: str = "mongodb://localhost:27017"
    database_name: str = "remedic_connect"
    secret_key: str = "change_me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
