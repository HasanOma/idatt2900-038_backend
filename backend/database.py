# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# import asyncio
# import databases
#
# Base = declarative_base()
#
# DATABASE_URL = "postgresql+psycopg2://mtp038:qwertY1!@mtp-db.postgres.database.azure.com:5432/postgres"
#
# engine = create_engine(DATABASE_URL)
#
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
#
# database = databases.Database(DATABASE_URL)
#
#
# async def initialize_database():
#     await database.connect()
#     Base.metadata.create_all(bind=engine)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine("postgresql+psycopg2://mtp038:qwertY1!@mtp-db.postgres.database.azure.com:5432/postgres",
            echo=True,
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async_db_session = AsyncDatabaseSession()