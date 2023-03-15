import asyncio
import json
from datetime import datetime

import redis
from channels.generic.websocket import AsyncWebsocketConsumer

from MTP_038_backend import api_ship_requests
from MTP_038_backend import api_weather


class Ship_locations(AsyncWebsocketConsumer):
    group_name = 'ship_locations_group'
    client = redis.Redis()
    client.set(group_name, 0)

    def get_group_size(self):
        val = self.client.get(self.group_name)
        print(val)
        return int(val)

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.is_running = True
        await self.send_current_location()
        self.client.set(self.group_name, self.get_group_size() + 1)
        if self.get_group_size() == 1:
            asyncio.create_task(self.send_ship_locations())

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            self.client.set(self.group_name, self.get_group_size() - 1)
            if self.get_group_size() == 0:
                self.is_running = False
        except KeyError:
            pass

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_current_location(self):
        message = await api_ship_requests.all_ships()
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_ship_locations(self):
        await api_ship_requests.main()
        start = datetime.now()
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
            elapsed_time = (datetime.now() - start).total_seconds() / 60
            if elapsed_time >= 26:
                await api_ship_requests.schedule_token()
                start = datetime.now()
                print(f"Elapsed time before resetting token: {elapsed_time}  minutes")
            if not self.is_running:
                print("Stopped sending ship locations")
                break


class Weather_data(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False

    async def connect(self):
        await self.accept()
        self.is_running = True
        while self.is_running:
            msg = await api_weather.weather_api()
            await self.send(text_data=json.dumps({
                'weather': msg
            }))
            await asyncio.sleep(900)

    async def disconnect(self, code):
        self.is_running = False