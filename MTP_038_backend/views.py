# from api_ship_requests import background_task
import numpy as np
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from MTP_038_backend import api_ship_requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from MTP_038_backend.serializers import UserSerializer, GroupSerializer, CoordinateSerializer


# background_task.apply_async()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CoordinateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        print(request.data)
        data = {
            'north': request.data.get('north'),
            'west': request.data.get('west'),
            'south': request.data.get('south'),
            'east': request.data.get('east')
        }
        serializer = CoordinateSerializer(data=data)
        print(data)
        if serializer.is_valid():
            api_ship_requests.set_coordinates(data['north'], data['west'], data['south'], data['east'])
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)