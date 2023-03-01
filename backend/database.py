from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio
Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
        self._initialized = False

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        if self._initialized:
            raise RuntimeError("AsyncDatabaseSession has already been initialized")

        self._engine = create_async_engine(
            "sqlite+aiosqlite:///db.sqlite3",
            echo=False,
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

        self._initialized = True

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async_db_session = AsyncDatabaseSession()

async def initialize_database():
    await async_db_session.init()
    await async_db_session.create_all()

# call the async function to initialize the database
asyncio.run(initialize_database())

# Now the session is initialized and can be used
session = async_db_session
