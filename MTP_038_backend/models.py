import asyncio
from sqlalchemy.orm import declarative_base
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import cursor, conn
from backend.database import sqlalchemy_conn_string

engine = create_engine(sqlalchemy_conn_string)
Session = sessionmaker(bind=engine)


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


class tuple_to_ship:
    def __init__(self, mmsi, name, msgtime, latitude, longitude, speedOverGround, shipType, destination, eta,
                 shipLength, shipWidth):
        self.mmsi = mmsi
        self.name = name
        self.msgtime = msgtime
        self.latitude = latitude
        self.longitude = longitude
        self.speedOverGround = speedOverGround
        self.shipType = shipType
        self.destination = destination
        self.eta = eta
        self.shipLength = shipLength
        self.shipWidth = shipWidth


class ModelAdmin:
    @classmethod
    async def create(cls, kwargs):
        if not isinstance(kwargs, dict):
            raise ValueError("Invalid argument: expected a dictionary")

        def quote_camelcase_columns(column_name):
            return f'"{column_name}"' if any(x.isupper() for x in column_name) else column_name

        quoted_keys = [quote_camelcase_columns(key) for key in kwargs.keys()]
        quoted_excluded_keys = [quote_camelcase_columns(key) for key in kwargs.keys() if key != 'mmsi']

        query = f"""
            INSERT INTO {cls.__tablename__} ({', '.join(quoted_keys)})
            VALUES ({', '.join(['%s'] * len(kwargs.values()))})
            ON CONFLICT (mmsi) DO UPDATE SET {', '.join([f'{key}=EXCLUDED.{key}' for key in quoted_excluded_keys])}
            RETURNING *
            """
        cursor.execute(query, tuple(kwargs.values()))
        result = cursor.fetchone()
        conn.commit()
        print("created ", result)
        return result

    @classmethod
    async def create_multi(cls, entities):
        for entity in entities:
            await cls.create(entity)

    @classmethod
    async def merge_token(cls, **kwargs):
        query = f"INSERT INTO {cls.__tablename__} ({', '.join(kwargs.keys())}) VALUES " \
                f"({', '.join(['%s'] * len(kwargs.values()))}) ON CONFLICT (id) DO UPDATE SET " \
                f"{', '.join([f'{key}=EXCLUDED.{key}' for key in kwargs.keys() if key != 'id'])} RETURNING *"
        cursor.execute(query, tuple(kwargs.values()))
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    async def update_ship_fields(cls, mmsi, fields):
        def quote_camelcase_columns(column_name):
            return f'"{column_name}"' if any(x.isupper() for x in column_name) else column_name

        quoted_keys = [quote_camelcase_columns(key) for key in fields.keys()]

        query = f"""
            UPDATE {cls.__tablename__}
            SET {', '.join(f'{k} = %s' for k in quoted_keys)}
            WHERE mmsi = %s
            RETURNING *
            """
        values = tuple(fields.values()) + (mmsi,)
        values = tuple([v if v is not None else '' for v in values])
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        return result

    @classmethod
    async def get(cls, id):
        query = f"SELECT * FROM {cls.__tablename__} WHERE mmsi = {id}"
        cursor.execute(query)
        result = cursor.fetchone()
        # print("result:", dict(result))
        if result is None:
            return None
        return result

    @classmethod
    async def get_basic(cls, id):
        query = f"SELECT * FROM {cls.__tablename__} WHERE mmsi = {id}"
        cursor.execute(query)
        result = cursor.fetchone()
        # print("result:", dict(result))
        if result is None:
            return None
        return result

    @classmethod
    async def get_token(cls, id):
        # print("getting ship ", id)
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
    speedOverGround = Column(Float(255), nullable=True,  name='speedOverGround')
    shipType = Column(Integer, nullable=True, name='shipType')
    destination = Column(String(255), nullable=True)
    eta = Column(String(255), nullable=True)
    shipLength = Column(Float, nullable=True, name='shipLength')
    shipWidth = Column(Float, nullable=True, name='shipWidth')

    __mapper_args__ = {"eager_defaults": True}

    def __eq__(self, other):
        if isinstance(other, Ship):
            return self.mmsi == other.mmsi
        return False

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mmsi': self.mmsi,
            'name': self.name,
            'msgtime': self.msgtime,
            'speedOverGround': self.speedOverGround,
            'destination': self.destination,
            'eta': self.eta,
            'shipType': self.shipType,
            'shipLength': self.shipLength,
            'shipWidth': self.shipWidth
        }


class Token(Base, ModelAdmin):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    bearer = Column(String(2000), nullable=True)
    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {
            'id': self.id,
            'bearer': self.bearer,
        }


class Weather:
    def __init__(self, weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]


async def migrate():
    Base.metadata.drop_all(engine)  # Drop all existing tables
    Base.metadata.create_all(engine)  # Recreate the tables with the new schema

if __name__ == "__main__":
    asyncio.run(migrate())
