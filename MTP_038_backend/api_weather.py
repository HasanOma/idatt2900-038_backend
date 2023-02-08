import asyncio
import aiohttp
import requests
import asgiref
from MTP_038_backend import models


async def weather_by_coordinates():
    latitude = 63.46
    longitude = 10.38