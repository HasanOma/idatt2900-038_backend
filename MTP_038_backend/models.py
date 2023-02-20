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


class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]

class Coordinate(models.Model):
    north: models.DecimalField(max_digits=14)
    west: models.DecimalField(max_digits=14)
    south: models.DecimalField(max_digits=14)
    east: models.DecimalField(max_digits=14)
