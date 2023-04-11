from django.urls import re_path
from MTP_038_backend import consumers

"""
routing.py

This module defines the WebSocket URL routing patterns for the Django project.
It maps WebSocket endpoints to their corresponding consumers (WebSocket handlers).

URL Patterns:
- ws/ship_locations/ : Map to the Ship_locations consumer to handle ship location data.
- ws/weather/        : Map to the Weather_data consumer to handle weather data.
"""

websocket_urlpatterns = [
    re_path(r'ws/ship_locations/$', consumers.Ship_locations.as_asgi()),
    re_path(r'ws/weather/$', consumers.Weather_data.as_asgi()),
]