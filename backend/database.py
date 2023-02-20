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
import databases

DATABASE_URL = "sqlite:///db.sqlite3"
database = databases.Database(DATABASE_URL)