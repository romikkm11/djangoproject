import os, sys, django
from methods import get_address_method_1, get_price_method_1, get_address_method_2
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')

django.setup()
load_dotenv()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

companies = [
    {
        'url' : os.getenv('URL_1'),
        'address_selector' : {'data-id': 'ef86798'},
        'get_address': get_address_method_1,
        'price_url' : os.getenv('URL_1_price'),
        'price_selector' : {'class' : 'elementor-tabs'},
        'get_price' : get_price_method_1,
        'min_prices_recording_sequence' : [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 1, 2, 3, 4, 5, 7, 8, 9, 10],
        'max_prices_recording_sequence' : [25, 36, 37, 38, 39, 50, 3, 4, 5, 10],
        'db_id' : 11

    }
#     {
#         'url' : os.getenv('URL_2'),
#         'address_selector' : {'class': 'footer-info'},
#         'get_address': get_address_method_2 
#     }
]