import os

import asyncio
import aiohttp
import requests
import asgiref
import json
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
# from backend.database import async_db_session
from MTP_038_backend.models import Ship
from MTP_038_backend.models import Vessel
from MTP_038_backend.models import Token
import ast
import os

#TODO 1: Bearer in db

bearer = None

def set_coordinates():
    # global filter_coordinates
    north = 64.299370
    west = 7.706847
    south = 63.210836
    east = 11.561208
    filter_coordinates = [
        [
            [west, north],
            [west, south],
            [east, south],
            [east, north],
            [west, north],
        ]
    ]
    return filter_coordinates
    print("new filter_coordinates   ", filter_coordinates)

async def token():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    # payload = os.getenv('token_payload')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # while True:
    await schedule_token(method_post, headers, 5, payload, url)

async def schedule_token(method, headers, interval, payload, url):
    global bearer
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            # print(api_response)
            bearer = api_response['access_token']
            token_to_db = Token(id=1, bearer=bearer)
            await Token.merge_token(id=1, bearer=bearer)
            # roken = await Token.get_token(1)
            # print("bearer from db ", roken.bearer)
    await asyncio.sleep(interval)

async def main():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    # payload = os.getenv('token_payload')
    print("payload ", payload)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    async with aiohttp.ClientSession() as session:
        async with session.request("POST", url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            bearer = api_response['access_token']
            token_to_db = Token(id=1, bearer=bearer)
            await Token.merge_token(id=1, bearer=bearer)
            # roken = await Token.get_token(1)
            # print("bearer from db 1 ", roken.bearer)

async def filter_ships():
    global bearer
    # global filter_coordinates

    url = "https://live.ais.barentswatch.no/v1/combined"

    payload = {
        "downsample": False,
        "modelType": "Full",
        "modelFormat": "Geojson",
        "geometry": {
            "type": "Polygon",
            "coordinates": set_coordinates()
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + bearer
    }
    now = datetime.now()
    start = now - timedelta(minutes=1)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                ships = []
                i = 0
                headers_dict = dict(response.headers)
                async for line in response.content:

                    event = line.decode('utf-8').strip()
                    fields = event.splitlines()
                    if fields:
                        try:
                            i += 1
                            data_dict = json.loads(fields[0])
                            data = Vessel(data_dict)
                            ship = Ship(**data.__dict__)
                            from_db = await Ship.get(ship.mmsi)
                            if from_db is None:
                                # print("appending ship", ship.to_dict())
                                ships.append(ship)
                            if i % 200 == 0:
                                entities = [ship.to_dict() for ship in ships]
                                await Ship.create_multi(entities)
                                ships = []
                            if i % 1050 == 0:
                                i = 0
                                print("sleeping")
                                await asyncio.sleep(300)
                            elapsed_time = (datetime.now() - start).total_seconds() / 60
                            if elapsed_time >= 26:
                                await token()
                                print("resetting token")
                                start = datetime.now()
                        except Exception as e:
                            print(f"Error processing JSON object: {data}. Error: {e}")
    except Exception as e:
        print(f"Error fetching data from {url}. Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    while True:
        asyncio.run(filter_ships())