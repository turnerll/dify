"""
Application configuration settings
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "222place"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False
    TESTING: bool = False
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-this-too"
    ENCRYPTION_KEY: str = "your-32-byte-encryption-key-for-sensitive-data"
    
    # CORS and Security
    CORS_ORIGINS: str = "http://localhost:3000,https://localhost:3000"
    TRUSTED_HOSTS: str = "localhost,127.0.0.1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/matchmaking_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    CACHE_DEFAULT_TIMEOUT: int = 300
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"
    CELERY_WORKER_CONCURRENCY: int = 4
    
    # Vector Database
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "user_embeddings"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # API Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 5000
    API_WORKERS: int = 4
    API_TIMEOUT: int = 60
    API_MAX_REQUEST_SIZE: str = "50MB"
    
    # Rate Limiting
    RATE_LIMIT_STORAGE_URL: str = "redis://redis:6379/3"
    RATE_LIMIT_DEFAULT: str = "100/hour"
    RATE_LIMIT_AUTH: str = "20/minute"
    RATE_LIMIT_MATCHING: str = "10/hour"
    
    # Matching Engine
    MATCHING_ALGORITHM: str = "hybrid"
    MATCHING_SIMILARITY_THRESHOLD: float = 0.7
    MATCHING_MAX_DISTANCE_KM: int = 50
    MATCHING_MAX_AGE_DIFFERENCE: int = 10
    MATCHING_DIVERSITY_FACTOR: float = 0.3
    RECOMMENDATIONS_COUNT: int = 10
    RECOMMENDATIONS_REFRESH_HOURS: int = 24
    EVENT_SUGGESTIONS_COUNT: int = 5
    
    # File Upload
    UPLOAD_FOLDER: str = "/app/uploads"
    MAX_CONTENT_LENGTH: str = "10MB"
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png,gif,pdf"
    STORAGE_TYPE: str = "local"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "/app/logs/app.log"
    LOG_MAX_SIZE: str = "100MB"
    LOG_BACKUP_COUNT: int = 5
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    FROM_EMAIL: str = "noreply@222place.local"
    FROM_NAME: str = "222.place"
    
    # Security and Privacy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_SPECIAL_CHARACTERS: bool = True
    PASSWORD_EXPIRY_DAYS: int = 90
    SESSION_TIMEOUT_MINUTES: int = 60
    REMEMBER_ME_DURATION_DAYS: int = 30
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    DATA_RETENTION_DAYS: int = 365
    INACTIVE_ACCOUNT_DAYS: int = 180
    MESSAGE_RETENTION_DAYS: int = 90
    
    # Content Moderation
    MODERATION_ENABLED: bool = True
    PROFANITY_FILTER_ENABLED: bool = True
    AUTO_MODERATION_THRESHOLD: float = 0.8
    
    # Feature Flags
    FEATURE_VECTOR_MATCHING: bool = True
    FEATURE_EVENT_SUGGESTIONS: bool = True
    FEATURE_GROUP_CHAT: bool = True
    FEATURE_VIDEO_CHAT: bool = False
    FEATURE_PUSH_NOTIFICATIONS: bool = True
    FEATURE_EMAIL_NOTIFICATIONS: bool = True
    
    # Localization
    DEFAULT_TIMEZONE: str = "UTC"
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,es"
    
    # External Services
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    HEALTH_CHECK_ENABLED: bool = True
    METRICS_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()