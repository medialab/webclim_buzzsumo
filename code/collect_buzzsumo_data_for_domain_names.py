import os
from datetime import datetime, timedelta
import csv
import sys
import time

from dotenv import load_dotenv
import requests

from domain_name_lists import MISINFORMATION_DOMAIN_NAMES_3
from buzzsumo_columns_to_keep import BUZZSUMO_COLUMNS_TO_KEEP


if __name__=="__main__":

    domain_name_list = MISINFORMATION_DOMAIN_NAMES_3
    begin_date_st = '2019-01-01'
    collection_period_length = 365 * 2 + 1
    # We collect the data for 2019 and 2020, so 365 * 2 + 1 days as 2020 was a leap year.

    load_dotenv()
    params = {
        'api_key': os.getenv('BUZZSUMO_API_KEY'),
        'num_results': 100
    }

    output_name = sys.argv[1] if len(sys.argv) >= 2 else 'articles.csv'
    output_path = os.path.join('.', 'data', 'buzzsumo_domain_name', output_name)
    f = open(output_path, 'w')

    output_2_name = sys.argv[1].split('.')[0] + '_nb.csv' if len(sys.argv) >= 2 else 'articles_nb.csv'
    output_2_path = os.path.join('.', 'data', 'buzzsumo_domain_name', output_2_name)
    g = open(output_2_path, 'w')

    with f:

        writer = csv.writer(f)
        writer.writerow(['date'] + BUZZSUMO_COLUMNS_TO_KEEP)

        with g:
            writer_2 = csv.writer(g)
            writer_2.writerow(['domain_name', 'date', 'article_number'])   

            for domain_name in domain_name_list:

                params['q'] = domain_name
                print('\n\n########################   ', domain_name.upper(), '   ########################\n')

                begin_date = datetime.strptime(begin_date_st, '%Y-%m-%d')

                for date_index in range(collection_period_length):

                    if begin_date.day == 1:
                        print('\n  ', begin_date.strftime("%Y-%m-%d"))
                    params['begin_date'] = begin_date.timestamp()
                    params['end_date'] = (begin_date + timedelta(days=1)).timestamp()

                    api_call_attempt = 0

                    while True:

                        # if first try, add a sleep function so that we wait at least 1.05 seconds between two calls (see later code)
                        if api_call_attempt == 0:
                            start_call_time = time.time()
                        # if second try or more, wait an exponential time
                        else: 
                            time.sleep(2**(api_call_attempt - 1))
                        
                        r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)
                        status_code = r.status_code
                        if (begin_date.day == 1) and ('X-RateLimit-Month-Remaining' in r.headers.keys()):
                            print('Remaining number of calls for this month:', r.headers['X-RateLimit-Month-Remaining'])
                        print('Call status code:', status_code)

                        if status_code == 420:
                            print("-----------------------   PAUSE   -----------------------")
                            time.sleep(1800)

                        if api_call_attempt == 0:
                            end_call_time = time.time()
                            if (end_call_time - start_call_time) < 1.2:
                                time.sleep(1.2 - (end_call_time - start_call_time))

                        if status_code == 200:
                            break

                        api_call_attempt += 1

                    for result in r.json()['results']:
                        writer.writerow([begin_date.date()] + [result[column_name] for column_name in BUZZSUMO_COLUMNS_TO_KEEP])
                    writer_2.writerow([domain_name, begin_date.date(), int(r.json()['total_results'])])

                    begin_date += timedelta(days=1)
