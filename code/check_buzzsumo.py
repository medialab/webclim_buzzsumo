import os
from datetime import datetime

from dotenv import load_dotenv
import requests


if __name__=="__main__":

    load_dotenv()

    params = {
        'api_key': os.getenv('BUZZSUMO_API_KEY'),
        'q': 'lemonde.fr',
    }

    r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)

    print(r.json()['results'])
    print(r.headers)
    print(r.status_code)