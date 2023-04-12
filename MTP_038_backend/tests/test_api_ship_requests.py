from unittest.mock import patch
import aiohttp
import asynctest
from MTP_038_backend import api_ship_requests
from MTP_038_backend.api_ship_requests import create_or_update_ship_with_basic
from MTP_038_backend.api_ship_requests import schedule_all_ships
from MTP_038_backend.api_ship_requests import schedule_token


class TestApiShipRequests(asynctest.TestCase):

    async def test_set_coordinates(self):
        api_ship_requests.set_coordinates()
        coordinates = api_ship_requests.coordinates

        # Check if coordinates have been set correctly
        self.assertEqual(coordinates['north'], 64.299370)
        self.assertEqual(coordinates['west'], 7.706847)
        self.assertEqual(coordinates['south'], 63.210836)
        self.assertEqual(coordinates['east'], 11.561208)

    async def test_check_specific_coordinates(self):
        api_ship_requests.set_coordinates()

        # Test some coordinates within the specified range
        self.assertTrue(api_ship_requests.check_specific_coordinates(63.5, 9.0))
        self.assertTrue(api_ship_requests.check_specific_coordinates(64.0, 10.0))

        # Test some coordinates outside the specified range
        self.assertFalse(api_ship_requests.check_specific_coordinates(62.0, 9.0))
        self.assertFalse(api_ship_requests.check_specific_coordinates(65.0, 10.0))

    async def test_schedule_token(self):
        # Call the schedule_token method
        result = await schedule_token()

        # Assert that the result is a non-empty string (access token)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    @patch('MTP_038_backend.api_ship_requests.set_coordinates')
    async def test_main_coordinates(self, mock_set_coordinates):
        await api_ship_requests.main()
        # Check if set_coordinates() has been called
        mock_set_coordinates.not_called()

    @patch('MTP_038_backend.api_ship_requests.schedule_token')
    async def test_main_token(self, mock_schedule_token):
        await api_ship_requests.main()
        # Check if schedule_token() has been called
        mock_schedule_token.not_called()

    async def setUp(self):
        self.ship_data = {
            'mmsi': 123456789,
            'name': 'Updated Test Ship',
            'msgtime': '2023-03-15T12:00:00Z',
            'latitude': 64.299370,
            'longitude': 7.706847,
            'speedOverGround': 5.0,
            'shipType': 10
        }

    @patch('MTP_038_backend.models.Ship.get_basic')
    @patch('MTP_038_backend.models.Ship.update_ship_fields')
    @patch('MTP_038_backend.models.Ship.create')
    async def test_create_or_update_ship_with_basic(self, mock_create, mock_update, mock_get_basic):
        # Set the return values for the mocked functions
        mock_get_basic.return_value = None
        mock_create.return_value = tuple(self.ship_data.values())
        mock_update.return_value = tuple(self.ship_data.values())

        # Call the create_or_update_ship_with_basic method with the ship data
        result = await create_or_update_ship_with_basic(self.ship_data)

        # Assert that the result is a tuple with the expected values
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[:7], tuple(self.ship_data.values()))

    async def test_schedule_all_ships(self):
        bearer = 'test'
        results = []
        url = "https://live.ais.barentswatch.no/v1/latest/combined"
        method = "GET"
        payload = "{}"
        headers = {'Authorization': f'Bearer {bearer}'}

        async with aiohttp.ClientSession() as session:
            results = await schedule_all_ships(method, headers, payload, url, session, results)

        # None because bearer is wrong
        self.assertIsNone(results)


if __name__ == '__main__':
    asynctest.main()
