from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ShipLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def send_ship_location(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        pass