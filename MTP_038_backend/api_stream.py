import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import namedtuple
from datetime import datetime

import aiohttp
import requests

# from backend.database import async_db_session
from MTP_038_backend.models import Ship
from MTP_038_backend.models import Token
from MTP_038_backend.models import Vessel



#TODO 1: Bearer in db

bearer = None

def set_coordinates():
    """
    Create and return a list of coordinates defining a polygon for filtering ship data.

    Returns:
        list: A list of lists containing coordinates (longitude, latitude) of the polygon.
    """
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
    """
    Asynchronously obtain an access token and update the global 'bearer' variable and the Token database.
    """
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    # payload = os.getenv('token_payload')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # while True:
    await schedule_token(method_post, headers, 5, payload, url)

async def schedule_token(method, headers, interval, payload, url):
    """
    Asynchronously schedule the token retrieval at a specified interval.

    Args:
        method (str): The HTTP request method, typically "POST".
        headers (dict): The HTTP request headers.
        interval (int): The time interval (in seconds) for scheduling the token retrieval.
        payload (str): The request payload containing client_id, scope, client_secret, and grant_type.
        url (str): The URL to request the access token from.
    """
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
    """
    Authenticate with the BarentsWatch API and obtain an access token.

    This function sends a POST request to the BarentsWatch API to obtain an
    access token using the provided client credentials. The obtained token is
    then saved in the global `bearer` variable and updated in the database.
    """
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
    """
    Fetch ship data from the BarentsWatch API and filter the results.

    This function fetches ship data from the BarentsWatch API using the
    access token obtained from the `main` function. It filters the ships
    based on their destination and estimated time of arrival (ETA). If a ship's
    destination or ETA has changed, it will be added to the `ships` list. The
    filtered ships are then saved to the database in batches.
    """
    global bearer
    # global filter_coordinates

    Skip = namedtuple('Skip',
                      ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType', 'destination',
                       'eta', 'shipLength', 'shipWidth'])

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
                            date_format = "%m%d%H%M"
                            try:
                                date_obj = datetime.strptime(ship.eta, date_format)
                                now = datetime.now()
                                date_obj = date_obj.replace(year=now.year)
                                date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                                ship.eta = date_str
                            except:
                                date_str = None
                                ship.eta = date_str
                            if from_db is None:
                                # print("appending ship", ship.to_dict())
                                ships.append(ship)
                            else:
                                from_db = dict(zip(Skip._fields, from_db))
                                if from_db["destination"] != ship.destination:
                                    ships.append(ship)
                                elif from_db["eta"] != ship.eta:
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