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