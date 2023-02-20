from django.db import models

# Create your models here.
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

class Ship(Model):
    mmsi = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, null = True)
    msgtime = fields.CharField(max_length=255, null=True)
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
    speedOverGround = fields.FloatField(null=True)
    courseOverGround = fields.FloatField(null=True)
    navigationalStatus = fields.IntField(null=True)
    rateOfTurn = fields.FloatField(null=True)
    shipType = fields.IntField(null=True)
    trueHeading = fields.IntField(null=True)
    callSign = fields.CharField(max_length=255, null=True)
    destination = fields.CharField(max_length=255, null=True)
    eta = fields.CharField(max_length=255, null=True)
    imoNumber = fields.IntField(null=True)  # Add this line
    dimensionA = fields.IntField(null=True)
    dimensionB = fields.IntField(null=True)
    dimensionC = fields.IntField(null=True)
    dimensionD = fields.IntField(null=True)
    draught = fields.FloatField(null=True)
    shipLength = fields.FloatField(null=True)
    shipWidth = fields.FloatField(null=True)
    positionFixingDeviceType = fields.IntField(null=True)
    reportClass = fields.CharField(max_length=255, null=True)

    def save_to_database(self):
        # Check if the object already exists in the database
        try:
            ship = Ship.objects.get(mmsi=self.mmsi)
        except Ship.DoesNotExist:
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
        ship.save()

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]

class Coordinate(models.Model):
    north: models.DecimalField(max_digits=14)
    west: models.DecimalField(max_digits=14)
    south: models.DecimalField(max_digits=14)
    east: models.DecimalField(max_digits=14)
