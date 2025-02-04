import os, sys, django
# 
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itproger1.settings')

django.setup()
load_dotenv()
import methods
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

companies = [
    {
        'url' : os.getenv('URL_1'),
        'address_selector' : {'data-id': 'ef86798'},
        'get_address': methods.get_address_method_1,
        'price_url' : os.getenv('URL_1_price'),
        'price_selector' : {'class' : 'elementor-tabs'},
        'get_price' : methods.get_price_method_1,
        'min_prices_recording_sequence' : [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 1, 2, 3, 4, 5, 7, 8, 9, 10],
        'max_prices_recording_sequence' : [24, 36, 37, 38, 39, 50, 3, 4, 5, 10],
        'db_id' : 11

    },
# #     {
# #         'url' : os.getenv('URL_2'),
# #         'address_selector' : {'class': 'footer-info'},
# #         'get_address': get_address_method_2 
# #     },
    {
        'url' : os.getenv('URL_3'),
        'address_selector' : {'class' : 'header-address text-left'},
        'get_address': methods.get_address_method_3,
        'price_url' : os.getenv('URL_3_price'),
        'price_selector' : 'tbody',
        'get_price' : methods.get_price_method_3,
        'min_prices_recording_sequence' : [11, 52, 14, 28, 19, 24, 37, 38, 48, 47, 61, 1, 2, 3, 5, 32, 36, 7, 9, 55, 56, 62],
        'max_prices_recording_sequence' : [19, 37, 38],
        'db_id' : 13
    },
    {
        'url' : os.getenv('URL_4'),
        'address_selector' : {'id': 'location_name_2'},
        'get_address': methods.get_address_method_4,
        'price_url' : os.getenv('URL_4'),
        'price_selector' : { 'data-artboard-recid' : '300063382' },
        'get_price' : methods.get_price_method_4,
        'min_prices_recording_sequence' : [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
        'db_id' : 14
    },
    {
        'url' : os.getenv('URL_5'),
        'address_selector' : {'class' : 't-descr_sm'},
        'get_address': methods.get_address_method_5,
        'price_url' : os.getenv('URL_5'),
        'price_selector' : { 'data-artboard-recid' : '330275433' },
        'get_price' : methods.get_price_method_5,
        'min_prices_recording_sequence' : [63, 70, 81, 68, 82, 77, 64, 83, 72, 65, 74, 73],
        'db_id' : 15
    }   
]