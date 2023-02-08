import asyncio
import aiohttp
import asgiref
import requests
async def weather_api():


    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

    querystring = {"altitude": "5", "lat": "63.46", "lon": "10.38"}

    payload = ""
    headers = {
        "User-Agent": "Marine_Traffic_Portal_BachelorOppgaveNTNU/1.0"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)

asyncio.run(weather_api())