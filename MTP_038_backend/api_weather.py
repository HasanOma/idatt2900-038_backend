import asyncio
import json
import random

import requests

from MTP_038_backend import models


async def weather_api():


    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

    querystring = {"altitude": "5", "lat": "63.46", "lon": "10.38"}

    payload = ""

    names = ["MarineTrafficAnalysisSystem/1.0 (NTNU Bachelor Thesis)",
             "PortalMonitoringSoftware/1.0 NTNU_Project",
             "BachelorThesis_MarineTrafficTracker/1.0 (NTNU)",
             "MarineVesselMonitoring/1.0 (Bachelor Study NTNU)",
             "NTNU_MarineTrafficPortal/1.0 (Bachelor Thesis Research)",
             "AccentureMarineTrafficSystem/1.0"
             "Accenture_MarineMonitoring/1.0",
             "MarineTrafficPortal_Accenture_v1.0",
             "Accenture_VesselTracking/1.0",
             "Accenture_MarineTrafficAnalysis/1.0",
             "Marine_Traffic_Portal_BachelorOppgaveNTNU/1.0",
             "MarineTrafficMonitoringSystem_NTNU/1.0",
             "NTNU_MarineTrafficAnalysis_Portal/1.0",
             "BachelorThesis_MarineVesselTracking/1.0",
             "NTNU_MarineTrafficMonitoring/1.0",
             "MarineTrafficAnalysis_Accenture/1.0",
             "Accenture_MarineTrafficTracker/1.0",
             "MarineTrafficPortal_NTNU_v1.0",
             "Accenture_MarineTrafficSystem_v1.0",
             "MarineTrafficAnalysis_BachelorThesisNTNU/1.0",
             "Accenture_MarineVesselMonitoring/1.0"
             ]

    headers = {
        "User-Agent": random.choice(names)
    }
    print(headers)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    weather_data = json.loads(response.text)

    data = models.Weather(weather_data)
    data_dict = vars(data)

    return data_dict