from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio
import databases

Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://mtp038:qwertY1!@mtp-db.postgres.database.azure.com:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

database = databases.Database(DATABASE_URL)


async def initialize_database():
    await database.connect()
    Base.metadata.create_all(bind=engine)

database = initialize_database()