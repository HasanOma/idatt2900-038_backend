from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from django.db import models
from sqlalchemy import update as sqlalchemy_update

from backend.database import Base, async_db_session, session

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

class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        instance = cls(**kwargs)
        async_db_session.add(instance)
        await async_db_session.commit()
        return instance

    @classmethod
    async def create_multi(cls, ships):
        # print("creating ships ", ships)
        async with async_db_session.begin():
            for ship in ships:
                await async_db_session.merge(ship)
            await async_db_session.commit()

    @classmethod
    async def update_ship_fields(cls, mmsi, fields):
        async with async_db_session.begin():
            update_query = update(cls).where(cls.mmsi == mmsi).values(fields)
            await async_db_session.execute(update_query)
            query = select(cls).where(cls.mmsi == mmsi)
            result = await async_db_session.execute(query)
            return result.scalar()

    @classmethod
    async def get(cls, id):
        async with async_db_session.begin():
            query = select(cls).where(cls.mmsi == id)
            result = await async_db_session.execute(query)
            res = result.scalar()
            result.close()
            return res

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

    def __eq__(self, other):
        if isinstance(other, Ship):
            return self.mmsi == other.mmsi
        return False

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

class token(Base, ModelAdmin):
    __tablename__ = 'api_token'
    id = Column(Integer, primary_key=True)
    bearer = Column(String(255), nullable=True)
    __mapper_args__ = {"eager_defaults": True}

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]