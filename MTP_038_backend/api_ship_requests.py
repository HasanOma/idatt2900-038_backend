# from __future__ import absolute_import, unicode_literals
import asyncio
import aiohttp
import requests
import asgiref
import json
from typing import Dict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from MTP_038_backend import models
from backend.database import session
from MTP_038_backend.models import Ship
# from celery import shared_task

bearer = None
coordinates = {
"north": 1.0,
"west": 1.0,
"south": 1.0,
"east": 1.0
}

filter_coordinates = [
    [
        [9.704635339617539, 63.71636867949894],
        [9.713635278804048, 63.27997175643682],
        [11.420623744565347, 63.29076081515623],
        [11.897620521465939, 63.945256790972905],
        [11.453623521583495, 64.12388902116183],
        [10.097632684107396, 63.852867195619694],
        [9.704635339617539, 63.71636867949894]
    ]
]

top_right = [64.08, 11.47]
top_left = [63.6, 9.56]
bottom_right = [63.98, 12.01]
bottom_left = [63.16, 10.03]

def set_coordinates(north, west, south, east):
    global coordinates
    global filter_coordinates
    coordinates['north'] = north
    coordinates['west'] =  west
    coordinates['south'] = south
    coordinates['east'] = east
    filter_coordinates = [
        [
            [west, north],
            [west, south],
            [east, south],
            [east, north],
            [west, north],
        ]
    ]
    print("new coordinates: ", coordinates.values() )
    print("new filter_coordinates   ", filter_coordinates)

def check_coordinates_valid():
    global coordinates
    return coordinates != { "north": 1.0, "west": 1.0, "south": 1.0, "east": 1.0 }

def check_specific_coordinates(latitude, longitude):
    global coordinates
    north = coordinates['north']
    south = coordinates['south']
    west = coordinates['west']
    east = coordinates['east']
    if coordinates['north'] >= latitude >=coordinates['south'] and coordinates['west'] <= longitude <= coordinates['east']:
        return True
    else:
        return False

def check_coordinates(latitude, longitude):
    top_right = [64.08, 11.47]
    top_left = [63.6, 9.56]
    bottom_right = [63.98, 12.01]
    bottom_left = [63.16, 10.03]
    if (latitude <= top_right[0] and latitude >= bottom_left[0] and
        longitude <= top_right[1] and longitude >= bottom_left[1]):
        return True
    else:
        return False

async def schedule_token(method, headers, interval, payload, url):
    global bearer
    await asyncio.sleep(interval)
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            print(api_response)
            bearer = api_response['access_token']

async def token():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    while True:
        await schedule_token(method_post, headers, 3200, payload, url)

async def schedule_all_ships(method, headers, interval, payload, url, session, list_of_ships):
    await asyncio.sleep(interval)
    try:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            for data in api_response:
                latitude = data['latitude']
                longitude = data['longitude']
                if check_coordinates_valid():
                    if check_specific_coordinates(latitude, longitude):
                        ship = models.ship_request(data)
                        list_of_ships.append(vars(ship))
                elif check_coordinates(latitude, longitude):
                    ship = models.ship_request(data)
                    list_of_ships.append(vars(ship))
    except Exception as e:
        print(f"Error during API request: {e}")
        return []
    print(f"Number of ships: {len(list_of_ships)}")
    return list_of_ships

async def all_ships():
    global bearer
    url = "https://live.ais.barentswatch.no/v1/latest/combined"
    method = "GET"
    payload = "{}"
    headers = {'Authorization': f'Bearer {bearer}'}
    async with aiohttp.ClientSession() as session:
        while True:
            list_of_ships = []
            return await schedule_all_ships(method, headers, 0, payload, url, session, list_of_ships)

# @shared_task
async def main():
    # print("here3")
    # await connect_to_db()
    global bearer
    url = "https://id.barentswatch.no/connect/token"

    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    async with aiohttp.ClientSession() as session:
        async with session.request("POST", url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            bearer = api_response['access_token']
    asyncio.create_task(token())


async def filter_ships():
    global bearer

    global filter_coordinates

    url = "https://live.ais.barentswatch.no/v1/combined"

    payload = {
        "downsample": False,
        "modelType": "Full",
        "modelFormat": "Geojson",
        "geometry": {
            "type": "Polygon",
            "coordinates": filter_coordinates
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + bearer
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Unexpected response status: {response.status}")
                content_length = int(response.headers.get("Content-Length", 0))
                chunk_size = max(content_length // 100, 4096)  # at least 2048 bytes
                async for chunk in response.content.iter_chunked(chunk_size):
                    json_objects = chunk.decode("utf-8").split("\n")
                    for obj in json_objects:
                        if not obj:
                            continue
                        try:
                            data_return = json.loads(obj)
                            ship = models.Vessel(data_return)

                            data_ = Ship(mmsi=ship.mmsi,
                                            name=ship.name,
                                            msgtime=ship.msgtime,
                                            latitude=ship.latitude,
                                            longitude=ship.longitude,
                                            speedOverGround=ship.speedOverGround,
                                            courseOverGround=ship.courseOverGround,
                                            navigationalStatus=ship.navigationalStatus,
                                            rateOfTurn=ship.rateOfTurn,
                                            shipType=ship.shipType,
                                            trueHeading=ship.trueHeading,
                                            callSign=ship.callSign,
                                            destination=ship.destination,
                                            eta=ship.eta,
                                            imoNumber=ship.imoNumber,
                                            dimensionA=ship.dimensionA,
                                            dimensionB=ship.dimensionB,
                                            dimensionC=ship.dimensionC,
                                            dimensionD=ship.dimensionD,
                                            draught=ship.draught,
                                            shipLength=ship.shipLength,
                                            shipWidth=ship.shipWidth,
                                            positionFixingDeviceType=ship.positionFixingDeviceType,
                                            reportClass=ship.reportClass)

                            await add_ship(data_)
                            return data_.__dict__
                        except Exception as e:
                            print(f"Error processing JSON object: {obj}. Error: {e}")
    except Exception as e:
        print(f"Error fetching data from {url}. Error: {e}")

async def add_ship(ship):
    query = select(Ship).where(Ship.mmsi == ship.mmsi)
    result_proxy = await session.execute(query)
    existing_ship = result_proxy.fetchone()

    if existing_ship is not None:
        print("ship exists")
        # A ship with this mmsi already exists
        return

    new_ship = Ship(mmsi=ship.mmsi,
                    name=ship.name,
                    msgtime=ship.msgtime,
                    latitude=ship.latitude,
                    longitude=ship.longitude,
                    speedOverGround=ship.speedOverGround,
                    courseOverGround=ship.courseOverGround,
                    navigationalStatus=ship.navigationalStatus,
                    rateOfTurn=ship.rateOfTurn,
                    shipType=ship.shipType,
                    trueHeading=ship.trueHeading,
                    callSign=ship.callSign,
                    destination=ship.destination,
                    eta=ship.eta,
                    imoNumber=ship.imoNumber,
                    dimensionA=ship.dimensionA,
                    dimensionB=ship.dimensionB,
                    dimensionC=ship.dimensionC,
                    dimensionD=ship.dimensionD,
                    draught=ship.draught,
                    shipLength=ship.shipLength,
                    shipWidth=ship.shipWidth,
                    positionFixingDeviceType=ship.positionFixingDeviceType,
                    reportClass=ship.reportClass)

    return session.add(new_ship)
    try:
        await sync_to_async(session.commit)()
        print("Ship added to database")
    except IntegrityError:
        await sync_to_async(session.rollback)()
        print("Integrity error occurred. Ship not added to database.")

if __name__ == '__main__':
    asyncio.run(filter_ships())

#todo make models for the ship data we want to send to frontend
#todo photo api
#todo historic data for those ships