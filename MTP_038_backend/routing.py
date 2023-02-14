from django.urls import re_path
from MTP_038_backend import consumers

websocket_urlpatterns = [
    re_path(r'ws/filtered_ships/', consumers.Filtered_Ships.as_asgi()),
    re_path(r'ws/ship_locations/', consumers.Ship_locations.as_asgi()),
    re_path(r'ws/weather/', consumers.Weather_data.as_asgi())
]