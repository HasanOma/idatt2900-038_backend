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
from backend.database import async_db_session
from MTP_038_backend.models import Ship
from MTP_038_backend.models import ship_basic
# from celery import shared_task

bearer = None
coordinates = {
"north": 1.0,
"west": 1.0,
"south": 1.0,
"east": 1.0
}

#TODO Gj;r ALT modul'rt og sett forskjellige api i sin egen fil. legg bearer i db og coordinater!

top_right = [64.08, 11.47]
top_left = [63.6, 9.56]
bottom_right = [63.98, 12.01]
bottom_left = [63.16, 10.03]

def set_coordinates(north, west, south, east):
    global coordinates
    coordinates['north'] = north
    coordinates['west'] =  west
    coordinates['south'] = south
    coordinates['east'] = east
    print("new coordinates: ", coordinates.values() )

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

async def init_db():
    await async_db_session.init()
    await async_db_session.create_all()

async def all_ships():

    global bearer
    url = "https://live.ais.barentswatch.no/v1/latest/combined"
    method = "GET"
    payload = "{}"
    headers = {'Authorization': f'Bearer {bearer}'}
    async with aiohttp.ClientSession() as session:
        while True:
            list_of_ships = []
            return  await schedule_all_ships(method, headers, 4, payload, url, session, list_of_ships)

async def check_ship_coordinates(ship, boundary_coordinates):
    latitude = ship['latitude']
    longitude = ship['longitude']
    if (boundary_coordinates['north'] >= latitude >= boundary_coordinates['south'] and
        boundary_coordinates['west'] <= longitude <= boundary_coordinates['east']):
        return True
    else:
        return False

async def schedule_all_ships(method, headers, interval, payload, url, session, boundary_coordinates):
    await asyncio.sleep(interval)
    try:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            tasks = []
            for ship in api_response:
                latitude = ship['latitude']
                longitude = ship['longitude']
                if check_coordinates_valid():
                    if check_specific_coordinates(latitude, longitude):
                        # if ship and check_ship_coordinates(ship, boundary_coordinates):
                        new_ship = await create_or_update_ship_with_basic(ship)
                        tasks.append(new_ship)
                elif check_coordinates(latitude, longitude):
                    new_ship = await create_or_update_ship_with_basic(ship)
                    tasks.append(new_ship)
            results = tasks
            print(f"Number of ships: {len(results)}")
            return results
    except Exception as e:
        print(f"Error during API request: {e}")
        return []

async def create_or_update_ship_with_basic(ship):
    fields_to_update = {
        "msgtime": ship['msgtime'],
        "latitude": ship['latitude'],
        "longitude": ship['longitude'],
        "speedOverGround": ship['speedOverGround'],
        "shipType": ship['shipType']
    }
    new_ship = Ship(mmsi=ship['mmsi'],
                    name=ship['name'],
                    msgtime=ship['msgtime'],
                    latitude=ship['latitude'],
                    longitude=ship['longitude'],
                    speedOverGround=ship['speedOverGround'],
                    shipType=ship['shipType'])
    db_ship = await Ship.get(ship['mmsi'])
    if db_ship is not None:
        await db_ship.update_ship_fields(mmsi=ship['mmsi'], fields=fields_to_update)
        updated_ship = await Ship.get(ship['mmsi'])
        return updated_ship.to_dict()
    else:
        new_ship_dict = new_ship.__dict__
        new_ship_dict.pop('_sa_instance_state', None)
        created_ship = await Ship.create(mmsi=ship['mmsi'], name=ship['name'], **fields_to_update)
        return created_ship.to_dict()



# async def schedule_all_ships(method, headers, interval, payload, url, session, list_of_ships):
#     await asyncio.sleep(interval)
#     try:
#         async with session.request(method, url, data=payload, headers=headers) as resp:
#             api_response = await resp.json()
#             for data in api_response:
#                 if data:
#                     mmsi = int(data['mmsi'])
#                     latitude = data['latitude']
#                     longitude = data['longitude']
#                     if check_coordinates_valid():
#                         if check_specific_coordinates(latitude, longitude):
#                             from_db = await Ship.get(mmsi)
#                             if from_db is not None:
#                                 print("\n\n\n\n\ from_db _________________         ", from_db.to_dict(), "\n\n\n\n\n")
#                                 data_ = models.VesselBasic(data)
#                                 ship_ = ship_basic(**data_.__dict__)
#                                 from_db = await update_ship_with_basic(ship_)
#                                 print("\n\n\n\n\ new from_db _________________         ", from_db.to_dict(), "\n\n\n\n\n")
#                                 list_of_ships.append(from_db.to_dict())
#                             else:
#                                 print("\n\n\n\n\ ikke fra db !!!!!!!!!! _________________         ", "\n\n\n\n\n")
#                                 ship = await create_ship_with_basic(data)
#                                 list_of_ships.append(ship.to_dict())
#                     elif check_coordinates(latitude, longitude):
#                         from_db = await Ship.get(mmsi)
#                         if from_db is not None:
#                             print("\n\n\n\n\ from_db _________________         ", from_db.to_dict(), "\n\n\n\n\n")
#                             data_ = models.VesselBasic(data)
#                             ship_ = ship_basic(**data_.__dict__)
#                             from_db = await update_ship_with_basic(ship_)
#                             print("\n\n\n\n\ new from_db _________________         ", from_db.to_dict(), "\n\n\n\n\n")
#                             list_of_ships.append(from_db.to_dict())
#                         else:
#                             print("\n\n\n\n\ ikke fra db !!!!!!!!!! _________________         ", "\n\n\n\n\n")
#                             ship = await create_ship_with_basic(data)
#                             list_of_ships.append(ship.to_dict())
#     except Exception as e:
#         print(f"Error during API request: {e}")
#         return []
#     print(f"Number of ships: {len(list_of_ships)}")
#     return list_of_ships

# async def create_ship_with_basic(ship):
#     new_ship = Ship(mmsi=ship['mmsi'],
#                     name=ship['name'],
#                     msgtime=ship['msgtime'],
#                     latitude=ship['latitude'],
#                     longitude=ship['longitude'],
#                     speedOverGround=ship['speedOverGround'],
#                     courseOverGround=ship['courseOverGround'],
#                     rateOfTurn=ship['rateOfTurn'],
#                     shipType=ship['shipType'],
#                     trueHeading=ship['trueHeading'])
#     new_ship_dict = new_ship.__dict__
#     new_ship_dict.pop('_sa_instance_state', None)
#     return await Ship.create(**new_ship_dict)
#
# async def update_ship_with_basic(ship):
#     fields_to_update = {
#         "msgtime": ship.msgtime,
#         "latitude": ship.latitude,
#         "longitude": ship.longitude,
#         "speedOverGround": ship.speedOverGround,
#         "courseOverGround": ship.courseOverGround,
#         "rateOfTurn": ship.rateOfTurn,
#         "shipType": ship.shipType,
#         "trueHeading": ship.trueHeading
#     }
#     return await Ship.update_ship_fields(mmsi=ship.mmsi, fields=fields_to_update)