from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=settings.mode,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)

