from django.db import models
from sqlalchemy import Column, Integer, String, Float
from backend.database import engine
from sqlalchemy.ext.declarative import declarative_base
# Create your models here.

Base = declarative_base()

class ship_request:
    def __init__(self, data):
        self.courseOverGround = data['courseOverGround']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.name = data['name']
        self.rateOfTurn = data['rateOfTurn']
        self.shipType = data['shipType']
        self.speedOverGround = data['speedOverGround']
        self.trueHeading = data['trueHeading']
        self.mmsi = data['mmsi']
        self.msgtime = data['msgtime']

class res_data:
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

class Ship(Base):
    __tablename__ = 'ship'

    mmsi = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    msgtime = Column(String(255), nullable=True)
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

    def save_to_database(self, session):
        # Check if the object already exists in the database
        ship = session.query(Ship).get(self.mmsi)
        if not ship:
            # If the object does not exist, create a new one
            ship = Ship(mmsi=self.mmsi)

        # Update the object attributes
        ship.imoNumber = self.imoNumber
        ship.name = self.name
        ship.msgtime = self.msgtime
        ship.speedOverGround = self.speedOverGround
        ship.courseOverGround = self.courseOverGround
        ship.navigationalStatus = self.navigationalStatus
        ship.rateOfTurn = self.rateOfTurn
        ship.shipType = self.shipType
        ship.trueHeading = self.trueHeading
        ship.callSign = self.callSign
        ship.destination = self.destination
        ship.eta = self.eta
        ship.dimensionA = self.dimensionA
        ship.dimensionB = self.dimensionB
        ship.dimensionC = self.dimensionC
        ship.dimensionD = self.dimensionD
        ship.draught = self.draught
        ship.shipLength = self.shipLength
        ship.shipWidth = self.shipWidth
        ship.positionFixingDeviceType = self.positionFixingDeviceType
        ship.reportClass = self.reportClass

        # Save the updated or new object to the database
        session.add(ship)
        session.commit()

Base.metadata.create_all(engine)

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]

class Coordinate(models.Model):
    north: models.DecimalField(max_digits=14)
    west: models.DecimalField(max_digits=14)
    south: models.DecimalField(max_digits=14)
    east: models.DecimalField(max_digits=14)
