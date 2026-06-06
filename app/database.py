from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Create the async engine (the connection to PostgreSQL)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Session factory — each request gets its own session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class all models will inherit from


class Base(DeclarativeBase):
    pass

# Dependency — used in routes to get a DB session


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
