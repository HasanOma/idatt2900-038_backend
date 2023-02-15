import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from MTP_038_backend import api_ship_requests
from MTP_038_backend import api_weather

class Filtered_Ships(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await api_ship_requests.main()
        while True:
            message = await api_ship_requests.filter_ships()
            # print(message)
            await self.send(text_data=json.dumps({
                'message': message
            }))

            # Add a delay to avoid sending messages too frequently


    async def disconnect(self, close_code):
        pass

class Ship_locations(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await api_ship_requests.main()
        while True:
            message = await api_ship_requests.all_ships()
            # print(message)
            await self.send(text_data=json.dumps({
                'message': message
            }))
            # Add a delay to avoid sending messages too frequently

    async def disconnect(self, close_code):
        pass

class Weather_data(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await api_ship_requests.main()
        while True:
            msg = await api_weather.weather_api()
            print(msg, " 2")
            await self.send(text_data=json.dumps({
                'weather': msg
            }))
            await asyncio.sleep(900)
    async def disconnect(self, code):
        pass