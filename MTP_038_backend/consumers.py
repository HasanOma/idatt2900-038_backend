import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from MTP_038_backend import api_ship_requests
from MTP_038_backend import api_weather
from MTP_038_backend import api_stream
from backend.database import session

class Ship_locations(AsyncWebsocketConsumer):
    group_name = 'ship_locations_group'

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.is_running = True
        await self.send_current_location()
        if len(self.channel_layer.groups[self.group_name]) == 1:
            asyncio.create_task(self.send_ship_locations())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_current_location(self):
        await api_ship_requests.main()
        message = await api_ship_requests.all_ships()
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_ship_locations(self):
        while self.is_running:
            message = await api_ship_requests.all_ships()
            print(message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_message',
                    'message': message
                }
            )

            await asyncio.sleep(3)



class Filtered_Ships(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False

    async def connect(self):
        await self.accept()
        await api_stream.main()
        self.is_running = True
        while self.is_running:
            await api_stream.filter_ships()

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

# class Ship_locations(AsyncWebsocketConsumer):
#     group_name = 'ship_locations_group'
#
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         self.is_running = True
#         if len(self.channel_layer.groups[self.group_name]) == 1:
#             await self.send_ship_locations()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#
#     async def send_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#     async def send_ship_locations(self):
#         await api_ship_requests.main()
#         while self.is_running:
#             message = await api_ship_requests.all_ships()
#             print(message)
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     'type': 'send_message',
#                     'message': message
#                 }
#             )
#
#             await asyncio.sleep(1)