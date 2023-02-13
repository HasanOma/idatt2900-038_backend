import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from MTP_038_backend import api_ship_requests
from MTP_038_backend import api_weather

class ShipLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await api_ship_requests.main()
        while True:
            message = await api_ship_requests.filter_ships()
            print(message)
            await self.send(text_data=json.dumps({
                'message': message
            }))

            # Add a delay to avoid sending messages too frequently


    async def disconnect(self, close_code):
        pass


class Weather_data(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            msg = await api_weather.weather_api()
            print(msg, " 2")
            await self.send(text_data=json.dumps({
                'weather': msg
            }))
            await asyncio.sleep(900)
    async def disconnect(self, code):
        pass

# class ShipLocationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#         # sleep(2)
#         message = await tasks.main()
#             # api_requests.all_ships_from_other_file()
#
#         # await
#
#         print(message)
#
#         message = await tasks.all_ships()
#
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#     async def send_ship_location(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'messag': 'heipaadei'
#         }))
#
#     async def disconnect(self, close_code):
#         pass