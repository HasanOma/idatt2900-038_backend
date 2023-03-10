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
from collections import namedtuple
# from backend.database import async_db_session
from MTP_038_backend.models import Ship
from MTP_038_backend.models import Token
from MTP_038_backend.models import tuple_to_ship
import os
# from MTP_038_backend.models import ship_basic
# from celery import shared_task

bearer = None
coordinates = {
"north": 1.0,
"west": 1.0,
"south": 1.0,
"east": 1.0
}

def set_coordinates():
    global coordinates
    north = 64.299370
    west = 7.706847
    south = 63.210836
    east = 11.561208
    coordinates['north'] = north
    coordinates['west'] =  west
    coordinates['south'] = south
    coordinates['east'] = east

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

async def schedule_token():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    # payload = os.getenv('token_payload')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_from_db = await Token.get_token(1)
    if token_from_db is None:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=payload, headers=headers) as resp:
                api_response = await resp.json()
                print(api_response)
                bearer = api_response['access_token']
    else:
        bearer = token_from_db[1]
        # print("token from db ", token_from_db)
        # print("token from db ** ", **token_from_db)

async def main():
    set_coordinates()
    await schedule_token()

async def all_ships():
    global bearer
    url = "https://live.ais.barentswatch.no/v1/latest/combined"
    method = "GET"
    payload = "{}"
    headers = {'Authorization': f'Bearer {bearer}'}
    async with aiohttp.ClientSession() as session:
        while True:
            list_of_ships = []
            results = await schedule_all_ships(method, headers, payload, url, session, list_of_ships)
            return results

async def schedule_all_ships(method, headers, payload, url, session, results):
    Skip = namedtuple('tuple_to_ship',{'mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType', 'destination', 'eta', 'shipLength', 'shipWidth'})
    try:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            for ship in api_response:
                latitude = ship['latitude']
                longitude = ship['longitude']
                if check_specific_coordinates(latitude, longitude):
                    new_ship = await create_or_update_ship_with_basic(ship)
                    results.append(dict(zip(Skip._fields, new_ship)))
            print(f"Number of ships: {len(results)}")
            return results
    except Exception as e:
        print(f"Error during API request: {e}")
        return

async def create_or_update_ship_with_basic(ship):
    fields_to_update = {
        "msgtime": ship['msgtime'],
        "latitude": ship['latitude'],
        "longitude": ship['longitude'],
        "speedOverGround": ship['speedOverGround']
    }
    new_ship = Ship(mmsi=ship['mmsi'],
                    name=ship['name'],
                    msgtime=ship['msgtime'],
                    latitude=ship['latitude'],
                    longitude=ship['longitude'],
                    speedOverGround=ship['speedOverGround'],
                    shipType=ship['shipType'],
                    destination= None,
                    eta = None,
                    shipLength = None,
                    shipWidth = None,
    )
    if new_ship.speedOverGround is None:
        new_ship.speedOverGround = 0
    if fields_to_update['speedOverGround'] is None:
        fields_to_update['speedOverGround'] = 0
    db_ship = await Ship.get_basic(new_ship.mmsi)
    if db_ship is not None:
        print("db_ship ", db_ship)
        if round(db_ship[3], 3) == round(new_ship.latitude, 3) and round(db_ship[4], 3) == round(
                new_ship.longitude, 3):
            print("ship is the same", db_ship)
            return db_ship
        else:
            print("updating ship", new_ship.__dict__)
            return await Ship.update_ship_fields(mmsi=new_ship.mmsi, fields=fields_to_update)
    else:
        print("creating ship", new_ship.__dict__)
        new_ship = new_ship.__dict__
        new_ship.pop('_sa_instance_state', None)
        return await Ship.create(new_ship)