"""
Core Configuration Module
Load settings from environment variables
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application Settings"""
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "dev-secret-key-change-in-production-minimum-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # App
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Upload
    UPLOAD_DIR: str = "src/uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Pydantic V2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env vars (DB credentials etc)
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
