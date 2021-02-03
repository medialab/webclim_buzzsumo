import os
from datetime import datetime, timedelta
import csv
import sys
import time

from dotenv import load_dotenv
import requests

from domain_name_lists import ESTABLISHED_NEWS_DOMAIN_NAMES
from buzzsumo_columns_to_keep import BUZZSUMO_COLUMNS_TO_KEEP


if __name__=="__main__":

    domain_name_list = ESTABLISHED_NEWS_DOMAIN_NAMES

    # We collect the data for 2019 and 2020, so 365 * 2 + 1 days as 2020 was a leap year.
    collection_period_length = 365 * 2 + 1

    load_dotenv()
    params = {
        'api_key': os.getenv('BUZZSUMO_API_KEY'),
        'num_results': 100
    }

    output_name = sys.argv[1] if len(sys.argv) >= 2 else 'articles.csv'
    output_path = os.path.join('.', 'data', 'buzzsumo_domain_name', output_name)
    f = open(output_path, 'w')

    with f:

        writer = csv.writer(f)
        writer.writerow(BUZZSUMO_COLUMNS_TO_KEEP)

        for domain_name in domain_name_list:

            params['q'] = domain_name
            print('\n\n', domain_name.upper(), '\n')

            begin_date = datetime.strptime('2019-01-01', '%Y-%m-%d')

            for date_index in range(collection_period_length):

                print(begin_date)
                params['begin_date'] = begin_date.timestamp()
                params['end_date'] = (begin_date + timedelta(days=1)).timestamp()

                api_call_attempt = 0
                status_code = 400

                while status_code != 200:

                    if api_call_attempt > 0:
                        time.sleep(2**(api_call_attempt - 1))
                    api_call_attempt += 1

                    r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)
                    status_code = r.status_code
                    print(status_code)

                for result in r.json()['results']:
                    writer.writerow([result[column_name] for column_name in BUZZSUMO_COLUMNS_TO_KEEP])

                begin_date += timedelta(days=1)
