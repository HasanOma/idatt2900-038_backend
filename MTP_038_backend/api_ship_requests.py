from collections import namedtuple

import aiohttp

from MTP_038_backend.models import Ship
from MTP_038_backend.models import Token

bearer = None
coordinates = {
"north": 1.0,
"west": 1.0,
"south": 1.0,
"east": 1.0
}


def set_coordinates():
    """
    Set the global coordinates variable to the specified values.

    This function sets the global `coordinates` dictionary to the specified north, south, east, and west values.
    """
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
    """
    Check if the given latitude and longitude are within the specified coordinates.

    Args:
        latitude (float): The latitude of the point to check.
        longitude (float): The longitude of the point to check.

    Returns:
        bool: True if the point is within the specified coordinates, False otherwise.
    """
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
    """
    Retrieve an access token from the database or request a new one.

    This function checks the database for a stored access token. If one is found, it is returned.
    If not, a new token is requested from the BarentsWatch API and returned.

    Returns:
        str: The access token.
    """
    global bearer
    url = "https://id.barentswatch.no/connect/token"
    method_post = "POST"
    payload = "client_id=hasanro%40stud.ntnu.no%3AMarine%20Traffic%20Portal&scope=ais&client_secret=heihei999!!!&grant_type=client_credentials"
    # payload = os.getenv('token_payload')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_from_db = await Token.get_token(1)
    if token_from_db is None:
        async with aiohttp.ClientSession() as session:
            async with session.request(method_post, url, data=payload, headers=headers) as resp:
                api_response = await resp.json()
                print(api_response)
                bearer = api_response['access_token']
                return bearer
    else:
        bearer = token_from_db[1]
        return bearer
        # print("token from db ", token_from_db)
        # print("token from db ** ", **token_from_db)


async def main():
    """
    Set coordinates and schedule token retrieval.

    This function sets the coordinates for the area of interest and schedules
    the token retrieval process.
    """
    set_coordinates()
    await schedule_token()


async def all_ships():
    """
    Fetch all ship data from the BarentsWatch API.

    This function sends a GET request to the BarentsWatch API using the access
    token obtained from the main function to fetch data for all ships. The
    fetched data is then filtered based on specific coordinates and returned.
    """
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
    """
    Fetch ship data from an API and filter the results based on specific coordinates.

    This function sends a request to the specified API using the provided method,
    headers, payload, and URL. It processes the API response, filtering ships based
    on their latitude and longitude. If a ship is within the specified coordinates,
    it calls the `create_or_update_ship_with_basic` function to create or update the
    ship in the database. The filtered ships are then added to the `results` list.

    Args:
        method (str): The HTTP method for the API request (e.g., "GET" or "POST").
        headers (dict): The headers to include in the API request.
        payload (dict): The payload to include in the API request, if applicable.
        url (str): The URL of the API endpoint.
        session (aiohttp.ClientSession): The aiohttp client session for making requests.
        results (list): A list to store the filtered ship data.

    Returns:
        list: The updated results list containing the filtered ships.
    """
    Skip = namedtuple('Skip',
                      ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType', 'destination',
                       'eta', 'shipLength', 'shipWidth'])
    try:
        async with session.request(method, url, data=payload, headers=headers) as resp:
            api_response = await resp.json()
            for ship in api_response:
                latitude = ship['latitude']
                longitude = ship['longitude']
                if check_specific_coordinates(latitude, longitude):
                    new_ship = await create_or_update_ship_with_basic(ship)
                    # print("new_ship ", new_ship)
                    results.append(dict(zip(Skip._fields, new_ship)))
            print(f"Number of ships: {len(results)}")
            return results
    except Exception as e:
        print(f"Error during API request: {e}")
        return


async def create_or_update_ship_with_basic(ship):
    """
    Create or update a ship in the database based on basic ship data.

    This function takes a ship dictionary containing basic ship data and either
    creates a new ship in the database or updates an existing ship's fields.
    If a ship with the same MMSI already exists in the database and its latitude
    and longitude match the new ship data, no changes are made. Otherwise, the
    ship's fields are updated in the database.

    Args:
        ship (dict): A dictionary containing basic ship data.

    Returns:
        dict: The created or updated ship's data as a dictionary.
    """
    # print("ship ", ship)
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
        # print("db_ship ", db_ship)
        if round(db_ship[3], 3) == round(new_ship.latitude, 3) and round(db_ship[4], 3) == round(
                new_ship.longitude, 3):
            # print("ship is the same", db_ship)
            return db_ship
        else:
            # print("updating ship", new_ship.__dict__)
            return await Ship.update_ship_fields(mmsi=new_ship.mmsi, fields=fields_to_update)
    else:
        # print("creating ship", new_ship.__dict__)
        new_ship = new_ship.__dict__
        new_ship.pop('_sa_instance_state', None)
        return await Ship.create(new_ship)