from django.contrib.auth.models import User, Group
from rest_framework import serializers
from MTP_038_backend import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.

    This serializer class extends the HyperlinkedModelSerializer and is
    responsible for converting User instances into JSON format. It includes
    the 'url', 'username', 'email', and 'groups' fields in the serialized
    output.
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Group model.

    This serializer class extends the HyperlinkedModelSerializer and is
    responsible for converting Group instances into JSON format. It includes
    the 'url' and 'name' fields in the serialized output.
    """
    class Meta:
        model = Group
        fields = ['url', 'name']