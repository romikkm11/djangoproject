import requests
from bs4 import BeautifulSoup
import os
import django
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) ###Шлях до кореневої папки для парсера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')
django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config')) ###Шлях до API геокодера

from news.models import Company
import config ###Імпорт файлу з API геокодера

###Функції для парсингу адреси    
def get_address_method_1(soup, company):
    return soup.find(attrs=company['address_selector']).find(None).text.strip().split('\n')[0]

def get_address_method_2(soup, company):
    elements = soup.find_all(attrs=company['address_selector'])
    return elements[1].text.strip()


companies = [
    {
        'url' : '',
        'address_selector' : {'data-id': 'ef86798'},
        'get_address': get_address_method_1 
    },
    {
        'url' : '',
        'address_selector' : {'class': 'footer-info'},
        'get_address': get_address_method_2 
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for company in companies:
    response = requests.get(company['url'], headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        company_name = soup.find('title').text.strip()
        try:
            # Виклик методу безпосередньо з параметрів компанії
            address_text = company['get_address'](soup, company)
        except AttributeError:
            print(f"Не вдалося отримати адресу для {company['url']}")
        # address_text = soup.find(attrs=company['address_selector']).find(None).text.strip().split('\n')[0]

        ##Геокодер

        url = 'https://geocode.search.hereapi.com/v1/geocode'

        params = {
            'q': address_text,
            'apiKey' : config.API_KEY,
            'limit': 1
        }


        response = requests.get(url, params=params)

        company_pos = response.json()['items'][0]['position']

        company_latitude = company_pos['lat']
        company_longititude = company_pos['lng'] 
   
        ###Оновлення запису в БД
        company, created = Company.objects.update_or_create(
                name=company_name,
                latitude = company_latitude,
                longititude = company_longititude
            )
    else:
        print(f"Помилка: не вдалося отримати дані, код статусу: {response.status_code}")
    print(company_name, company_latitude, company_longititude)