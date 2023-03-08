from django.contrib.auth.models import User, Group
from rest_framework import serializers
from MTP_038_backend import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class CoordinateSerializer(serializers.Serializer):
#     class Meta:
#         model = models.Coordinate
#         fields = ['north', 'west', 'south', 'east']