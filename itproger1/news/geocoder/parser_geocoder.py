import requests
from bs4 import BeautifulSoup
import os
import django
import sys

###Парсер
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')
django.setup()

from news.models import Service

url = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    service_name = soup.find('title').text.strip()
    address_text = soup.find(attrs={'data-id': 'ef86798'}).find(None).text.strip().split('\n')[0] 
else:
    print(f"Помилка: не вдалося отримати дані, код статусу: {response.status_code}")

###Геокодер
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

import config
url = 'https://geocode.search.hereapi.com/v1/geocode'

params = {
    'q': address_text,
    'apiKey' : config.API_KEY,
    'limit': 1
}


response = requests.get(url, params=params)

service_pos = response.json()['items'][0]['position']

service_latitude = service_pos['lat']
service_longititude = service_pos['lng'] 
 
###Оновлення запису в БД
service, created = Service.objects.update_or_create(
        name=service_name,
        latitude = service_latitude,
        longititude = service_longititude
    )