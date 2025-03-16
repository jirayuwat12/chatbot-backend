import os
import secrets
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, Field, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class SecuritySettings(BaseModel):
    """Security related settings."""

    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key used for token generation and encryption",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Minutes before access token expires")
    ALGORITHM: str = Field(default="HS256", description="Algorithm used for JWT encoding/decoding")
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"], description="List of allowed hosts")


class DatabaseSettings(BaseModel):
    """Database connection settings."""

    POSTGRES_SERVER: str = Field(default="localhost", description="PostgreSQL server hostname")
    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(default="postgres", description="PostgreSQL password")
    POSTGRES_DB: str = Field(default="chatbot_db", description="PostgreSQL database name")
    POSTGRES_PORT: str = Field(default="5432", description="PostgreSQL server port")
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class APISettings(BaseModel):
    """API related settings."""

    API_V1_STR: str = Field(default="/api/v1", description="API version 1 prefix")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key for LLM integration")
    OTHER_API_KEY: Optional[str] = Field(default=None, description="Any other API key needed")
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "http://localhost:8080"],
        description="List of CORS origins",
    )

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class LoggingSettings(BaseModel):
    """Logging configuration."""

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(levelname)s: %(asctime)s - %(name)s - %(message)s", description="Log message format"
    )


class Settings(BaseSettings):
    """Main settings class that includes all sub-settings."""

    # General settings
    PROJECT_NAME: str = Field(default="Chatbot Backend", description="Name of the project")
    ENVIRONMENT: AppEnvironment = Field(default=AppEnvironment.DEVELOPMENT, description="Application environment")
    DEBUG: bool = Field(default=True, description="Debug mode flag")

    # Include sub-settings
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: APISettings = Field(default_factory=APISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=True,
    )

    @validator("ENVIRONMENT", pre=True)
    def validate_environment(cls, v: Optional[str]) -> AppEnvironment:
        if not v:
            return AppEnvironment.DEVELOPMENT
        env = v.lower()
        if env in [e.value for e in AppEnvironment]:
            return AppEnvironment(env)
        raise ValueError(f"Invalid environment: {v}")

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == AppEnvironment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == AppEnvironment.PRODUCTION

    @property
    def is_test(self) -> bool:
        """Check if running in test mode."""
        return self.ENVIRONMENT == AppEnvironment.TEST

    class Config:
        env_prefix = ""


# Create a global settings instance
def get_settings() -> Settings:
    """Get application settings based on environment."""
    env = os.getenv("APP_ENVIRONMENT", "development").lower()
    settings = Settings(_env_file=f".env.{env}" if os.path.exists(f".env.{env}") else ".env")

    # Override with production settings
    if settings.is_production:
        settings.DEBUG = False
        settings.security.ALLOWED_HOSTS = ["api.yourdomain.com"]  # Update for production
        settings.api.CORS_ORIGINS = ["https://yourdomain.com"]  # Update for production

    return settings


# Export a singleton instance of settings
settings = get_settings()
