import requests, os, sys, django
from bs4 import BeautifulSoup
from companies_config import companies, headers

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')

django.setup()

from news.models import Price, Service, Company

for company in companies:
    
    response = requests.get(company['price_url'], headers=headers)
    response.encoding = 'utf-8'


    if response.status_code == 200:
          soup = BeautifulSoup(response.text, 'html.parser')
          if isinstance(company['price_selector'], dict):
             service_price_block = soup.find(attrs=company['price_selector'])
             print('Словник')
          else:
              service_price_block = soup.find(company['price_selector'])
              print('Не словник')
          company['get_price'](service_price_block)
          if len(company['get_price'](service_price_block)) == 2:

            for i, index  in zip(company['get_price'](service_price_block)[0], company['min_prices_recording_sequence']):
                 min_service_price = int(i)
                 price, created = Price.objects.update_or_create(
                              defaults={'min_price' : min_service_price},
                              company = Company.objects.get(id = company['db_id']),
                              service = Service.objects.get(id = index),
                            )
            
            for i, index  in zip(company['get_price'](service_price_block)[1], company['max_prices_recording_sequence']):
                 max_service_price = int(i)
                 price, created = Price.objects.update_or_create(
                              defaults={'max_price' : max_service_price},
                              company = Company.objects.get(id = company['db_id']),
                              service = Service.objects.get(id = index),
                            )
          else:
               for i, index  in zip(company['get_price'](service_price_block), company['min_prices_recording_sequence']):
                 min_service_price = int(i)
                 price, created = Price.objects.update_or_create(
                              defaults={'min_price' : min_service_price},
                              company = Company.objects.get(id = company['db_id']),
                              service = Service.objects.get(id = index),
                            )
         