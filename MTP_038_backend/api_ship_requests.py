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
# from backend.database import async_db_session
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
    # await init_db()

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
            return  await schedule_all_ships(method, headers, 2, payload, url, session, list_of_ships)

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
                else:
                    if check_coordinates(latitude, longitude):
                        new_ship = await create_or_update_ship_with_basic(ship)
                        tasks.append(new_ship)
            results = tasks
            print(f"Number of ships: {len(results)}")
            return results
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

async def create_or_update_ship_with_basic(ship):
    fields_to_update = {
        'mmsi': ship['mmsi'],
        'name': ship['name'],
        'msgtime': ship['msgtime'],
        'latitude': ship['latitude'],
        'longitude': ship['longitude'],
        'speedOverGround': ship['speedOverGround']
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
        db_ship_dict = dict(zip(('mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                                 'destination', 'eta', 'shipLength', 'shipWidth'), db_ship))
        db_to_ship = Ship(**db_ship_dict)
        if db_ship_dict['latitude'] == ship['latitude'] and db_ship_dict['longitude'] == ship['longitude']:
            # print(f"Ship with mmsi: {ship['mmsi']} is already in database")
            return db_ship_dict
        else:
            if db_to_ship is not None:
                print(f"Updating ship with mmsi: {ship['mmsi']}")
                db_to_ship.update_ship_fields(**fields_to_update)
                updated_ship = await Ship.get(ship['mmsi'])
                db_ship_dict = dict(
                    zip(('mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                         'destination', 'eta', 'shipLength', 'shipWidth'), updated_ship))
                return db_ship_dict
            else:
                # print(f"Creating new ship with mmsi: {ship['mmsi']}")
                created_ship = await Ship.create_from_basic(**fields_to_update)
                db_ship_dict = dict(zip(('mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                                 'destination', 'eta', 'shipLength', 'shipWidth'), created_ship))
                return db_ship_dict
    else:
        # print(f"Creating new ship with mmsi: {ship['mmsi']}")
        created_ship = await Ship.create_from_basic(**fields_to_update)
        db_ship_dict = dict(zip(('mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                                 'destination', 'eta', 'shipLength', 'shipWidth'), created_ship))
        return db_ship_dict