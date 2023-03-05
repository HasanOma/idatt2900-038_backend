import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from MTP_038_backend import api_ship_requests
from MTP_038_backend import api_weather
from MTP_038_backend import api_stream
# from backend.database import session

class Filtered_Ships(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False

    async def connect(self):
        await self.accept()
        await api_stream.main()
        self.is_running = True
        while self.is_running:
            message = await api_stream.filter_ships()
            print(message)
            await self.send(text_data=json.dumps({
                'message': message
            }))
            # Add a delay to avoid sending messages too frequently
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.is_running = False


class Ship_locations(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False

    async def connect(self):
        await self.accept()
        await api_ship_requests.main()
        self.is_running = True
        while self.is_running:
            message = await api_ship_requests.all_ships()
            print(message)
            await self.send(text_data=json.dumps({
                'message': message
            }))
            # Add a delay to avoid sending messages too frequently
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.is_running = False

class Weather_data(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False

    async def connect(self):
        await self.accept()
        self.is_running = True
        while self.is_running:
            msg = await api_weather.weather_api()
            print(msg, " 2")
            await self.send(text_data=json.dumps({
                'weather': msg
            }))
            await asyncio.sleep(900)

    async def disconnect(self, code):
        self.is_running = False
