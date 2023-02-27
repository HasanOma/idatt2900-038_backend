import asyncio
import aiohttp
import requests
import asgiref
import json
from typing import Dict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from MTP_038_backend import models
from backend.database import async_db_session
from MTP_038_backend.models import Ship

bearer = None
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

def set_coordinates(north, west, south, east):
    global filter_coordinates
    filter_coordinates = [
        [
            [west, north],
            [west, south],
            [east, south],
            [east, north],
            [west, north],
        ]
    ]
    print("new filter_coordinates   ", filter_coordinates)

async def init_db():
    await async_db_session.init()
    await async_db_session.create_all()

async def token():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    while True:
        await schedule_token(method_post, headers, 3200, payload, url)

async def schedule_token(method, headers, interval, payload, url):
    global bearer
    await asyncio.sleep(interval)
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            print(api_response)
            bearer = api_response['access_token']

async def main():
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
    await init_db()

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
                response_content = response.content
                while True:
                    chunk = await response_content.read(chunk_size)
                    if not chunk:
                        break
                    json_objects = chunk.decode("utf-8").split("\n")
                    for obj in json_objects:
                        if not obj:
                            continue
                        try:
                            data_return = json.loads(obj)
                            data_ = models.Vessel(data_return)
                            ship = Ship(**data_.__dict__)
                            from_db = await Ship.get(ship.mmsi)
                            # print("from db ", from_db.to_dict())
                            if from_db is None:
                                await create_ship(ship)
                            # print(data_.name)
                            return data_.__dict__
                        except Exception as e:
                            print(f"Error processing JSON object: {from_db}. Error: {e}")
    except Exception as e:
        print(f"Error fetching data from {url}. Error: {e}")

async def create_ship(ship):
    print("creating ship ", ship.to_dict())
    return await Ship.create(mmsi=ship.mmsi,
                    name=ship.name,
                    msgtime=ship.msgtime,
                    latitude=ship.latitude,
                    longitude=ship.longitude,
                    speedOverGround=ship.speedOverGround,
                    courseOverGround=ship.courseOverGround,
                    rateOfTurn=ship.rateOfTurn,
                    shipType=ship.shipType,
                    trueHeading=ship.trueHeading,
                    navigationalStatus=ship.navigationalStatus,
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

async def update_ship(mmsi, ship):
    print("updating ship ", ship.to_dict())
    return await Ship.update(mmsi, mmsi=ship.mmsi,
                    name=ship.name,
                    msgtime=ship.msgtime,
                    latitude=ship.latitude,
                    longitude=ship.longitude,
                    speedOverGround=ship.speedOverGround,
                    courseOverGround=ship.courseOverGround,
                    rateOfTurn=ship.rateOfTurn,
                    shipType=ship.shipType,
                    trueHeading=ship.trueHeading,
                    navigationalStatus=ship.navigationalStatus,
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