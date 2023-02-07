# from __future__ import absolute_import, unicode_literals
import asyncio
import aiohttp
import requests
import asgiref
from MTP_038_backend import models
# from celery import shared_task

bearer = None
list_of_ships = []

top_right = [64.08, 11.47]
top_left = [63.6, 9.56]
bottom_right = [63.98, 12.01]
bottom_left = [63.16, 10.03]

def check_coordinates(latitude, longitude, top_right, top_left, bottom_right, bottom_left):
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

async def schedule_all_ships(method, headers, interval, payload, url):
    global bearer
    global list_of_ships
    list_of_ships = []
    await asyncio.sleep(interval)
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            print(api_response)
            #send through websocket here
            for data in api_response:
                latitude = data['latitude']
                longitude = data['longitude']
                if check_coordinates(latitude, longitude, top_right, top_left, bottom_right, bottom_left):
                    print(f"({latitude}, {longitude}) I trondheimsfjorden!")
                    ship = models.Ship(data)
                    list_of_ships.append(vars(ship))
                else:
                    print(f"({latitude}, {longitude}) utenfor fjorden!")
    # for ship in list_of_ships:
    #     print(vars(ship))
    return list_of_ships
            # Do something with the API response


async def token():
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    while True:
        await schedule_token(method_post, headers, 3500, payload, url)

async def all_ships():
    print("here4")
    global bearer
    url = "https://live.ais.barentswatch.no/v1/latest/combined"
    method_post = "GET"
    payload = "{}"
    headers = {'Authorization': f'Bearer {bearer}'}
    while True:
        return await schedule_all_ships(method_post, headers, 2, payload, url)

# @shared_task
async def main():
    print("here3")
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
            print(bearer)
            # return bearer

    print(bearer)
    # task1 = asyncio.create_task(token())
    # task2 = asyncio.create_task(all_ships())
    # await asyncio.gather(task1, task2)

#todo filter ships in coordinates
#todo make models for the ship data we want to send to frontend
#todo get weather api
#todo photo api
#todo historic data for those ships

if __name__ == '__main__':
    asyncio.run(main())