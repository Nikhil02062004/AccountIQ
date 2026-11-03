import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    
    APP_NAME: str = "AccountIQ — Enterprise Intelligence"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./accountiq.db"
    
    # Optional LLM integration (Runs 100% reliably in zero-cost / no-key mode with DeterministicProvider)
    GEMINI_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "gemini-1.5-flash"
    
    # Privacy & Data Retention (GDPR / PDPA compliant)
    DATA_RETENTION_DAYS: int = 90
    ALLOW_CONTACT_DELETION: bool = True
    
    # Server configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings()
