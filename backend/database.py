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

def add(obj):
    session.add(obj)
    session.commit()

# Read (Retrieve) operation:
# ships = session.query(Ship).all()

#Update operation:
#ship = session.query(Ship).filter(Ship.mmsi == 123).first()
# ship.name = "new name"
# session.commit()

#Delete operation:
# ship = session.query(Ship).filter(Ship.mmsi == 123).first()
# session.delete(ship)
# session.commit()

# List operation:
# ships = session.query(Ship).all()
# for ship in ships:
#     print(ship.mmsi, ship.name)



