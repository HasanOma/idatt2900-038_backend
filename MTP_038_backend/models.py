from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from django.db import models

from backend.database import Base, async_db_session


class VesselBasic:
    def __init__(self, data):
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.mmsi = data['mmsi']
        self.name = data['name']
        self.msgtime = data['msgtime']
        self.speedOverGround = data['speedOverGround']
        self.courseOverGround = data['courseOverGround']
        self.shipType = data['shipType']
        self.trueHeading = data['trueHeading']

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mmsi': self.mmsi,
            'name': self.name,
            'msgtime': self.msgtime,
            'speedOverGround': self.speedOverGround,
            'courseOverGround': self.courseOverGround,
            'shipType': self.shipType,
            'trueHeading': self.trueHeading
        }


class ResData:
    def __init__(self, data):
        self.data = data


class Vessel:
    def __init__(self, data):
        self.latitude = data['geometry']['coordinates'][0]
        self.longitude = data['geometry']['coordinates'][1]
        self.mmsi = data['properties']['mmsi']
        self.name = data['properties']['name']
        self.msgtime = data['properties']['msgtime']
        self.speedOverGround = data['properties']['speedOverGround']
        self.courseOverGround = data['properties']['courseOverGround']
        self.navigationalStatus = data['properties']['navigationalStatus']
        self.rateOfTurn = data['properties']['rateOfTurn']
        self.shipType = data['properties']['shipType']
        self.trueHeading = data['properties']['trueHeading']
        self.callSign = data['properties']['callSign']
        self.destination = data['properties']['destination']
        self.eta = data['properties']['eta']
        self.imoNumber = data['properties']['imoNumber']
        self.dimensionA = data['properties']['dimensionA']
        self.dimensionB = data['properties']['dimensionB']
        self.dimensionC = data['properties']['dimensionC']
        self.dimensionD = data['properties']['dimensionD']
        self.draught = data['properties']['draught']
        self.shipLength = data['properties']['shipLength']
        self.shipWidth = data['properties']['shipWidth']
        self.positionFixingDeviceType = data['properties']['positionFixingDeviceType']
        self.reportClass = data['properties']['reportClass']

    def __eq__(self, other):
        if isinstance(other, Vessel):
            return self.mmsi == other.mmsi
        return False


class ship_basic(Base):
    __tablename__ = 'ship_basic'

    mmsi = Column(Integer, primary_key=True)
    msgtime = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speedOverGround = Column(Float, nullable=True)
    courseOverGround = Column(Float, nullable=True)
    name = Column(String(255), nullable=True)
    rateOfTurn = Column(Float, nullable=True)
    shipType = Column(Integer, nullable=True)
    trueHeading = Column(Integer, nullable=True)
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {"eager_defaults": True}

class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        instance = cls(**kwargs)
        async_db_session.add(instance)
        await async_db_session.commit()
        return instance


    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.mmsi == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.mmsi == id)
        result = await async_db_session.execute(query)
        return result.scalar()

    @classmethod
    async def get_by_mmsi(cls, id, name):
        query = select(cls).where(cls.mmsi == id and cls.name == name)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result

class Ship(Base, ModelAdmin):
    __tablename__ = 'ships'

    mmsi = Column(Integer, primary_key=True)
    name = Column(String(255))
    msgtime = Column(String(255))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speedOverGround = Column(Float, nullable=True)
    courseOverGround = Column(Float, nullable=True)
    navigationalStatus = Column(Integer, nullable=True)
    rateOfTurn = Column(Float, nullable=True)
    shipType = Column(Integer, nullable=True)
    trueHeading = Column(Integer, nullable=True)
    callSign = Column(String(255), nullable=True)
    destination = Column(String(255), nullable=True)
    eta = Column(String(255), nullable=True)
    imoNumber = Column(Integer, nullable=True)
    dimensionA = Column(Integer, nullable=True)
    dimensionB = Column(Integer, nullable=True)
    dimensionC = Column(Integer, nullable=True)
    dimensionD = Column(Integer, nullable=True)
    draught = Column(Float, nullable=True)
    shipLength = Column(Float, nullable=True)
    shipWidth = Column(Float, nullable=True)
    positionFixingDeviceType = Column(Integer, nullable=True)
    reportClass = Column(String(255), nullable=True)

    __mapper_args__ = {"eager_defaults": True}


class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]

class Coordinate(models.Model):
    north = models.DecimalField(max_digits=14, decimal_places=8)
    west = models.DecimalField(max_digits=14, decimal_places=8)
    south = models.DecimalField(max_digits=14, decimal_places=8)
    east = models.DecimalField(max_digits=14, decimal_places=8)

