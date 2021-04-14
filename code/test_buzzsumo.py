import os
from datetime import datetime, timedelta
import json

from dotenv import load_dotenv
import requests


if __name__=="__main__":

    load_dotenv()
    params = {
        'api_key': os.getenv('BUZZSUMO_API_KEY'),
        'q': 'lemonde.fr',
        'begin_date': (datetime.now() - timedelta(days=1)).timestamp(),
        'end_date': datetime.now().timestamp(),
        'num_results': 100,
    }
    print(json.dumps(params, indent=4))

    r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)
    print('Status code:', r.status_code)
    print('Headers:', r.headers)
    print(json.dumps(r.json(), indent=4))
