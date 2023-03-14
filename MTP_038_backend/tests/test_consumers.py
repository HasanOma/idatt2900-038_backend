# import asyncio
# from unittest.mock import patch
#
# from channels.testing import WebsocketCommunicator
# from django.test import TestCase
#
# from MTP_038_backend.consumers import Ship_locations, Weather_data
#
#
# class ShipLocationsConsumerTest(TestCase):
#     async def connect(self):
#         communicator = WebsocketCommunicator(Ship_locations.as_asgi(), '/')
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         return communicator
#
#     async def disconnect(self, communicator):
#         communicator.channel_layer = self.channel_layer
#         await communicator.disconnect()
#         self.assertFalse(communicator.channel_layer.groups.get('ship_locations_group', None))
#
#     async def test_connect(self):
#         communicator = await self.connect()
#         await self.disconnect(communicator)
#
#     async def test_send_current_location(self):
#         with patch('MTP_038_backend.api_ship_requests.all_ships') as mock_all_ships:
#             mock_all_ships.return_value = 'test_message'
#             communicator = await self.connect()
#             message = await communicator.receive_json_from()
#             self.assertEqual(message['message'], 'test_message')
#             await self.disconnect(communicator)
#
#     async def test_send_ship_locations(self):
#         with patch('MTP_038_backend.api_ship_requests.all_ships') as mock_all_ships, \
#                 patch('MTP_038_backend.api_ship_requests.schedule_token') as mock_schedule_token:
#             mock_all_ships.return_value = 'test_message'
#             mock_schedule_token.return_value = None
#             communicator = await self.connect()
#             await communicator.send_json_to({'type': 'send_ship_locations'})
#             message = await communicator.receive_json_from()
#             self.assertEqual(message['message'], 'test_message')
#             await communicator.send_json_to({'type': 'stop_send_ship_locations'})
#             await asyncio.sleep(1)
#             message = await communicator.receive_json_from()
#             self.assertFalse(message)
#             await self.disconnect(communicator)
#
#
# class WeatherDataConsumerTest(TestCase):
#     async def connect(self):
#         communicator = WebsocketCommunicator(Weather_data.as_asgi(), '/')
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)
#         return communicator
#
#     async def disconnect(self, communicator):
#         await communicator.disconnect()
#         self.assertFalse(communicator.is_running)
#
#     async def test_connect(self):
#         communicator = await self.connect()
#         await self.disconnect(communicator)
#
#     async def test_send_weather_data(self):
#         with patch('MTP_038_backend.api_weather.weather_api') as mock_weather_api:
#             mock_weather_api.return_value = 'test_message'
#             communicator = await self.connect()
#             message = await communicator.receive_json_from()
#             self.assertEqual(message['weather'], 'test_message')
#             await communicator.send_json_to({'type': 'stop_send_weather_data'})
#             await asyncio.sleep(1)
#             message = await communicator.receive_json_from()
#             self.assertFalse(message)
#             await self.disconnect(communicator)