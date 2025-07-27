from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:12345@localhost:5432/light"

# ✅ Create async engine without pool settings
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# ✅ Async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ✅ Base class for models
Base = declarative_base()

# ✅ Dependency for FastAPI


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
