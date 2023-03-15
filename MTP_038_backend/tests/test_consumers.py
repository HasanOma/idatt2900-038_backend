import json
import asyncio
from datetime import datetime
import asynctest
from unittest.mock import patch
from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from MTP_038_backend import api_ship_requests, api_weather
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the consumers you want to test
from MTP_038_backend.consumers import Ship_locations, Weather_data


# Define the mock functions
async def mocked_api_ship_requests_all_ships():
    return {'ship_data': 'test_ship_data'}


async def mocked_api_weather_weather_api():
    return {'weather_data': 'test_weather_data'}


class TestShipLocationsConsumer(asynctest.TestCase):
    @patch('MTP_038_backend.consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_connect(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    @patch('MTP_038_backend.consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_disconnect(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        print(await communicator.disconnect())
        self.assertIsNotNone(communicator)

    @patch('MTP_038_backend.consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_send_current_location(self):
        # First, connect to the websocket gives none as a response
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        # Simulate sending a request for the current location
        message = json.dumps({'type': 'send_current_location'})
        await communicator.send_json_to(json.loads(message))
        # Check if the received message matches the expected message
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message, {'message': None})
        await communicator.disconnect()


class TestWeatherDataConsumer(asynctest.TestCase):
    @patch('MTP_038_backend.consumers.api_weather.weather_api', new=mocked_api_weather_weather_api)
    async def test_connect(self):
        communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    @patch('MTP_038_backend.consumers.api_weather.weather_api', new=mocked_api_weather_weather_api)
    async def test_disconnect(self):
        communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
        await communicator.connect()
        await communicator.disconnect()

        self.assertIsNotNone(communicator)

    @patch('MTP_038_backend.consumers.api_weather.weather_api', new=mocked_api_weather_weather_api)
    async def test_weather_data_send(self):
        communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
        await communicator.connect()

        async def stop_weather_data_consumer():
            await asyncio.sleep(1)
            await communicator.disconnect()

        asyncio.ensure_future(stop_weather_data_consumer())

        received_message = await communicator.receive_json_from()
        self.assertIsInstance(received_message['weather']['temperature'], float)
        self.assertIsInstance(received_message['weather']['wind_speed'], float)
