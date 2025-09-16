"""
Database configuration and connection management
"""

import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
import structlog

from .settings import settings

logger = structlog.get_logger()

# Create database engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,
    poolclass=NullPool if settings.TESTING else None,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database connection and create tables if needed."""
    try:
        # Test connection
        async with engine.begin() as conn:
            # Import models to ensure they're registered
            from models import user, profile, onboarding, match, event, social, moderation
            
            # Create tables (in production, use Alembic migrations)
            if settings.DEBUG or settings.TESTING:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables created/verified")
            
        logger.info("Database connection established")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise

async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")