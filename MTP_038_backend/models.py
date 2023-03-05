# from sqlalchemy import Column, Integer, String, Float, text, update
# from sqlalchemy.orm import Session
# from django.db import models
#
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
# from backend.database import engine, SessionLocal






# class VesselBasic:
#     def __init__(self, data):
#         self.latitude = data['latitude']
#         self.longitude = data['longitude']
#         self.mmsi = data['mmsi']
#         self.timestamp = data['timestamp']
#
#     def to_dict(self):
#         return {
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'mmsi': self.mmsi,
#             'timestamp': self.timestamp,
#         }

class Vessel:
    def __init__(self, data):
        self.latitude = data['geometry']['coordinates'][0]
        self.longitude = data['geometry']['coordinates'][1]
        self.mmsi = data['properties']['mmsi']
        self.name = data['properties']['name']
        self.msgtime = data['properties']['msgtime']
        self.speedOverGround = data['properties']['speedOverGround']
        self.shipType = data['properties']['shipType']
        self.destination = data['properties']['destination']
        self.eta = data['properties']['eta']
        self.shipLength = data['properties']['shipLength']
        self.shipWidth = data['properties']['shipWidth']

    def __eq__(self, other):
        if isinstance(other, Vessel):
            return self.mmsi == other.mmsi
        return False

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from django.db import models
from sqlalchemy import update as sqlalchemy_update

# from backend.database import async_db_session
#
# class ModelAdmin:
#     @classmethod
#     async def create(cls, **kwargs):
#         instance = cls(**kwargs)
#         async_db_session.add(instance)
#         await async_db_session.commit()
#         return instance
#
#     @classmethod
#     async def create_multi(cls, ships):
#         async with async_db_session.begin():
#             async_db_session.add_all(ships)
#
#     @classmethod
#     async def update(cls, id, **kwargs):
#         query = (
#             sqlalchemy_update(cls)
#             .where(cls.mmsi == id)
#             .values(**kwargs)
#             .execution_options(synchronize_session="fetch")
#         )
#         await async_db_session.execute(query)
#         await async_db_session.commit()
#
#     @classmethod
#     async def update_ship_fields(cls, mmsi, fields):
#         update_query = update(cls).where(cls.mmsi == mmsi).values(fields)
#         await async_db_session.execute(update_query)
#         await async_db_session.commit()
#         query = select(cls).where(cls.mmsi == mmsi)
#         result = await async_db_session.execute(query)
#         return result.scalar()
#
#     @classmethod
#     async def get(cls, id):
#         query = select(cls).where(cls.mmsi == id)
#         result = await async_db_session.execute(query)
#         res = result.scalar()
#         result.close()
#         return res
#
#     @classmethod
#     async def get_by_mmsi(cls, id, name):
#         query = select(cls).where(cls.mmsi == id and cls.name == name)
#         results = await async_db_session.execute(query)
#         (result,) = results.one()
#         return result


from backend.database import cursor, conn

class ModelAdmin:
    @classmethod
    def create(cls, **kwargs):
        print("creating ship ", kwargs)
        query = f"INSERT INTO {cls.__tablename__} ({', '.join(kwargs.keys())}) VALUES ({', '.join(['%s'] * len(kwargs.values()))}) RETURNING *"
        cursor.execute(query, tuple(kwargs.values()))
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    async def create_from_basic(cls, **kwargs):
        print("creating ship from basic ", kwargs)
        fields = ", ".join(kwargs.keys())
        values = ", ".join([f"'{value}'" for value in kwargs.values()])
        query = f"INSERT INTO {cls.__tablename__} ({fields}) VALUES ({values}) RETURNING *"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    def update(cls, id, **kwargs):
        set_fields = ", ".join([f"{key}='{value}'" for key, value in kwargs.items()])
        query = f"UPDATE {cls.__tablename__} SET {set_fields} WHERE mmsi = {id} RETURNING *"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    def update_ship_fields(cls, **fields):
        query = f"UPDATE {cls.__tablename__} SET {', '.join(f'{k} = %s' for k in fields.keys())} WHERE mmsi = %s RETURNING *"
        values = tuple(fields.values()) + (fields['mmsi'],)
        values = tuple([v if v is not None else '' for v in values])
        cursor.execute(query, values)
        result = cursor.fetchone()
        print("update_ship_fields result:", result)
        conn.commit()
        return result

    @classmethod
    async def get(cls, id):
        print("getting ship ", id)
        query = f"SELECT * FROM {cls.__tablename__} WHERE mmsi = {id}"
        cursor.execute(query)
        result = cursor.fetchone()
        print("query:", query)
        print("result:", result)
        if result is None:
            return None
        return result

# class ModelAdmin:
#     @classmethod
#     async def create(cls, **kwargs):
#         print("creating ship ", kwargs)
#         query = cls.__table__.insert().values(**kwargs)
#         return await session.execute(query)
#
#     @classmethod
#     async def create_multi(cls, ships):
#         query = cls.__table__.insert().values(ships)
#         return await session.execute(query)
#
#     @classmethod
#     async def update(cls, id, **kwargs):
#         query = (
#             update(cls.__table__)
#             .where(cls.mmsi == id)
#             .values(**kwargs)
#         )
#         await session.execute(query)
#
#     @classmethod
#     async def update_ship_fields(cls, mmsi, fields):
#         query = (
#             cls.__table__.update()
#             .where(cls.mmsi == mmsi)
#             .values(fields)
#             .returning(text("*"))
#         )
#         result = await session.execute(query).one()
#
#         # update the instance in the session
#         instance = cls(**result)
#         for key, value in fields.items():
#             setattr(instance, key, value)
#         session2 = Session(bind=engine)
#         session2.merge(instance)
#         await session.commit()
#
#         return instance
#
#     @classmethod
#     async def get(cls, id):
#         query = session.query(cls).filter(cls.mmsi == id)
#         return await query.one_or_none()
#
#     @classmethod
#     async def get_by_mmsi(cls, id, name):
#         query = session.query(cls).filter(cls.mmsi == id, cls.name == name)
#         return await query.one_or_none()

class Ship(Base, ModelAdmin):
    __tablename__ = 'ships'

    mmsi = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    msgtime = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speedOverGround = Column(Float, nullable=True)
    shipType = Column(Integer, nullable=True)
    destination = Column(String(255), nullable=True)
    eta = Column(String(255), nullable=True)
    shipLength = Column(Float, nullable=True)
    shipWidth = Column(Float, nullable=True)

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {
        'latitude': self.latitude ,
        'longitude': self.longitude ,
        'mmsi': self.mmsi ,
        'name': self.name ,
        'msgtime': self.msgtime ,
        'speedOverGround': self.speedOverGround ,
        'destination': self.destination ,
        'eta': self.eta ,
        'shipType': self.shipType ,
        'shipLength': self.shipLength ,
        'shipWidth': self.shipWidth
        }

class ship_basic(Base, ModelAdmin):
    __tablename__ = 'ship_timestamp'

    mmsi = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timestamp = Column(String, nullable=True)

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mmsi': self.mmsi,
            'timestamp': self.timestamp,
        }

class token(Base, ModelAdmin):
    __tablename__ = 'api_token'
    id = Column(Integer, primary_key=True)
    bearer = Column(String(255), nullable=True)
    __mapper_args__ = {"eager_defaults": True}

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]

class Coordinate(models.Model):
    north = models.DecimalField(max_digits=14, decimal_places=8, null=True)
    west = models.DecimalField(max_digits=14, decimal_places=8, null=True)
    south = models.DecimalField(max_digits=14, decimal_places=8, null=True)
    east = models.DecimalField(max_digits=14, decimal_places=8, null=True)


