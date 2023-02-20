# import databases
# import asyncpg
#
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# database = databases.Database(DATABASE_URL)
#
# async def connect_to_db():
#     # Create an asyncpg connection pool
#     pool = await asyncpg.create_pool(DATABASE_URL)
#     database._conn = pool

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()