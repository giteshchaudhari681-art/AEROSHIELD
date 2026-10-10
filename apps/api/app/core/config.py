from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AEROSHIELD API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5434"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "aeroshield"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET_KEY: str = os.getenv("AEROSHIELD_JWT_SECRET", "a_very_secure_and_long_jwt_secret_key_that_exceeds_32_bytes_for_hs256")
    
    # Read CORS Origins from environment, defaulting to the specific public domain or localhost
    _cors_origins: str = os.getenv("AEROSHIELD_CORS_ORIGINS", "https://aeroshield.mycompany.com,http://localhost:5173")
    CORS_ORIGINS: list[str] = [x.strip() for x in _cors_origins.split(",")]
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    AEROSHIELD_ADMIN_USERNAME: str = "admin"
    AEROSHIELD_ADMIN_PASSWORD: str = "admin"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
