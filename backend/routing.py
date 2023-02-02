from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from backend import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/ship_location/", consumers.ShipLocationConsumer.as_asgi()),
    ])
})