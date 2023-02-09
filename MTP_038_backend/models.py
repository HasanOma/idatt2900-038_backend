from django.db import models

# Create your models here.
class Ship:
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

class Weather:
    def __init__(self,weather_data):
        self.temperature = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.wind_speed = weather_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]