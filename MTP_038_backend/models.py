from sqlalchemy import Column, Integer, String, Float, text, update
from sqlalchemy.orm import Session
from django.db import models

from sqlalchemy.ext.declarative import declarative_base

from backend.database import engine, database


Base = declarative_base()

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

class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        print("creating ship ", kwargs)
        query = cls.__table__.insert().values(**kwargs)
        return await database.execute(query)

    @classmethod
    async def create_multi(cls, ships):
        query = cls.__table__.insert().values(ships)
        return await database.execute(query)

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            update(cls.__table__)
            .where(cls.mmsi == id)
            .values(**kwargs)
        )
        await database.execute(query)

    @classmethod
    async def update_ship_fields(cls, mmsi, fields):
        query = (
            cls.__table__.update()
            .where(cls.mmsi == mmsi)
            .values(fields)
            .returning(text("*"))
        )
        result = await database.fetch_one(query)

        # update the instance in the session
        instance = cls(**result)
        for key, value in fields.items():
            setattr(instance, key, value)
        session = Session(bind=engine)
        session.merge(instance)
        await database.commit()

        return instance

    @classmethod
    async def get(cls, id):
        query = cls.__table__.select().where(cls.mmsi == id)
        return await database.fetch_one(query)

    @classmethod
    async def get_by_mmsi(cls, id, name):
        query = cls.__table__.select().where(cls.mmsi == id and cls.name == name)
        return await database.fetch_one(query)

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


