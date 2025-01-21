import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

import config
url = 'https://geocode.search.hereapi.com/v1/geocode'
address = 'м.Львів, проспект свободи 28'

params = {
    'q': address,
    'apiKey' : config.API_KEY,
    'limit': 1
}


response = requests.get(url, params=params)

pos = response.json()['items'][0]['position']

lat = pos['lat']
lon = pos['lng'] 

print(lat, lon) 