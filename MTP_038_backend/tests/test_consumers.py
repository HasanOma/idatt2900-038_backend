import json
import asyncio
from datetime import datetime
import unittest
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

class TestShipLocationsConsumer(unittest.TestCase):
    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_connect(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_disconnect(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        await communicator.disconnect()
        self.assertFalse(communicator.instance.is_running)

    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_receive(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        message = json.dumps({'test': 'test_message'})
        await communicator.send_json_to(message)
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message, json.loads(message))

    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_send_message(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        message = {'test': 'test_message'}
        await communicator.send_json_to(message)
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message['message'], message)

    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    async def test_send_current_location(self):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()
        await communicator.instance.send_current_location()
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message['message'], {'ship_data': 'test_ship_data'})

    @patch('consumers.api_ship_requests.all_ships', new=mocked_api_ship_requests_all_ships)
    @patch('consumers.api_ship_requests.main')
    @patch('consumers.api_ship_requests.schedule_token')
    async def test_send_ship_locations(self, mocked_schedule_token, mocked_main):
        communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
        await communicator.connect()

        async def stop_send_ship_locations():
            await asyncio.sleep(1)
            communicator.instance.is_running = False

        asyncio.create_task(stop_send_ship_locations())
        await communicator.instance.send_ship_locations()

        # Check if api_ship_requests.main() was called
        mocked_main.assert_called_once()

        # Check if at least one message was sent
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message['message'], {'ship_data': 'test_ship_data'})


class TestWeatherDataConsumer(unittest.TestCase):
    @patch('consumers.api_weather.weather_api', new=mocked_api_weather_weather_api)
    async def test_connect(self):
        communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    @patch('consumers.api_weather.weather_api', new=mocked_api_weather_weather_api)
    async def test_disconnect(self):
        communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
        await communicator.connect()
        await communicator.disconnect()
        self.assertFalse(communicator.instance.is_running)

# To run the tests, use the following command in your terminal:
# python -m unittest test_consumers.py
