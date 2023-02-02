from django.urls import re_path
from . import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import backend.routing

websocket_urlpatterns = [
    re_path(r'ws/ship_location/', consumers.ShipLocationConsumer.as_asgi())
]