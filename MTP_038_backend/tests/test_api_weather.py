import unittest
from unittest.mock import patch, MagicMock
import asyncio

from MTP_038_backend import api_weather, models


async def run_weather_api():
    return await api_weather.weather_api()


class TestWeatherAPI(unittest.TestCase):
    @patch('requests.request')
    @patch('MTP_038_backend.models.Weather')
    def test_weather_api_returns_dict(self, mock_weather, mock_request):
        mock_response = MagicMock()
        mock_response.text = '{"some": "data"}'
        mock_request.return_value = mock_response

        # create a dictionary with expected keys
        expected_data = {'temperature': 10, 'wind_speed': 5}

        # mock the Weather class to return the expected dictionary
        mock_weather.return_value.__dict__ = expected_data

        result = asyncio.run(run_weather_api())
        expected_keys = {'temperature', 'wind_speed'}
        for key in expected_keys:
            self.assertIn(key, result)


if __name__ == '__main__':
    unittest.main()
