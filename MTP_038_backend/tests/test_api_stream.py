import json
import asyncio
from datetime import datetime
from unittest.mock import patch, MagicMock
from django.test import TestCase
import asynctest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Ship, Token
from api_stream import (set_coordinates, token, schedule_token, main, filter_ships)  # Replace `your_module_name` with the appropriate import path

class TestSetCoordinates(TestCase):

    def test_set_coordinates(self):
        expected_coordinates = [
            [
                [7.706847, 64.299370],
                [7.706847, 63.210836],
                [11.561208, 63.210836],
                [11.561208, 64.299370],
                [7.706847, 64.299370],
            ]
        ]

        coordinates = set_coordinates()
        self.assertEqual(coordinates, expected_coordinates)

class TestTokenFunctions(TestCase):

    @patch('aiohttp.ClientSession')
    async def test_token(self, mock_client_session):
        mock_schedule_token = MagicMock()
        with patch('your_module_name.schedule_token', mock_schedule_token):
            await token()
            mock_schedule_token.assert_called_once_with("POST", {'Content-Type': 'application/x-www-form-urlencoded'}, 5, ANY, "https://id.barentswatch.no/connect/token")

    @patch('aiohttp.ClientSession')
    async def test_schedule_token(self, mock_client_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_client_session.return_value.__aenter__.return_value.request.return_value.__aenter__.return_value = mock_response

        await schedule_token("POST", {'Content-Type': 'application/x-www-form-urlencoded'}, 5, ANY, "https://id.barentswatch.no/connect/token")
        self.assertEqual(bearer, 'test_token')

class TestMain(TestCase):

    @patch('aiohttp.ClientSession')
    async def test_main(self, mock_client_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_client_session.return_value.__aenter__.return_value.request.return_value.__aenter__.return_value = mock_response

        await main()
        self.assertEqual(bearer, 'test_token')

class TestFilterShips(TestCase):

    @patch('aiohttp.ClientSession')
    async def test_filter_ships(self, mock_client_session):
        mock_response = MagicMock()
        mock_response.headers = {}
        mock_response.content = MagicMock()
        mock_response.content.__aiter__.return_value = iter([b'{"mmsi": 12345, "name": "Test Ship"}\n'])
        mock_client_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response

        with patch('models.Ship.get') as mock_ship_get, patch('models.Ship.create_multi') as mock_create_multi, patch('api_stream.datetime') as mock_datetime:
            mock_ship_get.return_value = None
            mock_datetime.now.return_value = datetime(2023, 1, 1)

            await filter_ships()

            mock_create_multi.assert_called_once_with([ANY])


if __name__ == '__main__':
    asynctest.main()