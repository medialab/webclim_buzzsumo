import os
from datetime import datetime, timedelta
import csv

from dotenv import load_dotenv
import requests


domain_name_list = [
    'cnn.com',
    'nytimes.com',
    'nbcnews.com',
    'dailymail.co.uk',
    'foxnews.com',
    'independent.co.uk',
    'bbc.com',
    'washingtonpost.com',
    'yahoo.com',
    'nypost.com'
]

# We collect the date for two years (2019 and 2020) plus one day, as 2020 was a leap year.
collection_period_length = 365 * 2 + 1

load_dotenv()
BUZZSUMO_API_KEY = os.getenv('BUZZSUMO_API_KEY')

params = {
    'api_key': BUZZSUMO_API_KEY,
    'num_results': 100
}

column_names = [
    'url',
    'published_date',
    'domain_name',
    'total_shares',
    'alexa_rank',
    'pinterest_shares',
    'total_reddit_engagements',
    'twitter_shares',
    'total_facebook_shares',
    'facebook_likes',
    'facebook_comments',
    'facebook_shares'
]

output_name = 'output_csv.csv'
output_path = os.path.join('.', 'data', 'buzzsumo_domain_name', output_name)
f = open(output_path, 'w')

with f:

    writer = csv.writer(f)
    writer.writerow(column_names)

    for domain_name in domain_name_list:

        params['q'] = domain_name
        print('\n\n', domain_name.upper(), '\n')

        begin_date = datetime.strptime('2019-01-01', '%Y-%m-%d')

        for date_index in range(collection_period_length):
            print(begin_date)

            params['begin_date'] = begin_date.timestamp()
            params['end_date'] = (begin_date + timedelta(days=1)).timestamp()

            r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)

            if r.status_code == 200:
                for result in r.json()['results']:
                    writer.writerow([result[column_name] for column_name in column_names])
            else: 
                print('ERROR', r.status_code, '\n')

            begin_date += timedelta(days=1)
