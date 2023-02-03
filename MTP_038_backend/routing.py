from django.urls import re_path
from MTP_038_backend import consumers

websocket_urlpatterns = [
    re_path(r'ws/ship_location/', consumers.ShipLocationConsumer.as_asgi())
]