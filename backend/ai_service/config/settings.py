from pydantic import BaseSettings


class Settings(BaseSettings):
    service_name: str = "ai_service"
    mongo_url: str = "mongodb://localhost:27017"
    database_name: str = "remedic_connect"
    secret_key: str = "change_me"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
