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

import psycopg2
# Update connection string information

host = 'mtp-db.postgres.database.azure.com'
dbname = "postgres"
user = "mtp038"
password = "qwertY1!"
sslmode = "require"
# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# conn.commit()
# cursor.close()
# conn.close()