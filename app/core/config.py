from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import secrets
from typing import Optional
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDAM ERP System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "pdam_erp"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        password = quote_plus(values.get('POSTGRES_PASSWORD', ''))
        return f"postgresql://{values.get('POSTGRES_USER')}:{password}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 