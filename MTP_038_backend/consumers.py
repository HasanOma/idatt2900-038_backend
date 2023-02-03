from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import api_requests

class ShipLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # sleep(2)
        message = await api_requests.main()
            # api_requests.all_ships_from_other_file()

        print(message)

        await self.send(text_data=json.dumps({
            'message': "message"
        }))

    async def send_ship_location(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'messag': 'heipaadei'
        }))

    async def disconnect(self, close_code):
        pass