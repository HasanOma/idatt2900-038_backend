from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from django.db import models
from sqlalchemy import update as sqlalchemy_update


from backend.database import cursor, conn

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
    def create(cls, **kwargs):
        # print("creating ship ", kwargs)
        query = f"INSERT INTO {cls.__tablename__} ({', '.join(kwargs.keys())}) VALUES ({', '.join(['%s'] * len(kwargs.values()))}) RETURNING *"
        cursor.execute(query, tuple(kwargs.values()))
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    async def create_multi(cls, ships):
        # print("creating ships ", ships)
        async with async_db_session.begin():
            for ship in ships:
                await async_db_session.merge(ship)
            await async_db_session.commit()

    @classmethod
    async def merge_token(cls, entity):
        # print("merging ships ", ships)
        async with async_db_session.begin():
            await async_db_session.merge(entity)
            await async_db_session.commit()

    @classmethod
    async def create_from_basic(cls, **kwargs):
        # print("creating ship from basic ", kwargs)
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
        # print("update_ship_fields result:", result)
        conn.commit()
        return result

    @classmethod
    async def get(cls, id):
        print("getting ship ", id)
        query = f"SELECT * FROM {cls.__tablename__} WHERE mmsi = {id}"
        cursor.execute(query)
        result = cursor.fetchone()
        # print("query:", query)
        # print("result:", result)
        if result is None:
            return None
        return result

    @classmethod
    async def get_token(cls, id):
        print("getting ship ", id)
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = {id}"
        cursor.execute(query)
        result = cursor.fetchone()
        # print("query:", query)
        # print("result:", result)
        if result is None:
            return None
        return result

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

class Token(Base, ModelAdmin):
    __tablename__ = 'api_token'
    id = Column(Integer, primary_key=True)
    bearer = Column(String(255), nullable=True)
    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {
        'bearer': self.bearer ,
        }

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]