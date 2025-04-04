from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings
from sqlalchemy.orm import DeclarativeBase
from databases import Database
from redis.client import Redis 
from core.config import settings

database = Database(settings.POSTGRES_CLEAR_URL)
clear_engine = create_engine(settings.POSTGRES_CLEAR_URL)
engine = create_async_engine(settings.POSTGRES_URL)

async_session_maker = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)

redis_session = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class Base(DeclarativeBase):
    metadata = MetaData()