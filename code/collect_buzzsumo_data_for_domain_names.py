import os
from datetime import datetime, timedelta
import csv

from dotenv import load_dotenv
import requests


# domain_name_example = 'nytimes.com'
domain_name_example = 'cnn.com'
# We collect the date for two years (2019 and 2020) plus one day, as 2020 was a leap year.
collection_period_length = 365 * 2 + 1

load_dotenv()
BUZZSUMO_API_KEY = os.getenv('BUZZSUMO_API_KEY')

params = {
    'q': domain_name_example,
    'api_key': BUZZSUMO_API_KEY,
    'num_results': 100
}

# NBC, The Daily Mail, CNN, Fox News, The Independent, BBC, The New York Times, The Washington Post, Yahoo and The New York Post
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

    begin_date = datetime.strptime('2019-01-01', '%Y-%m-%d')

    for date_index in range(collection_period_length):
        print(begin_date)

        params['begin_date'] = begin_date.timestamp()
        params['end_date'] = (begin_date + timedelta(days=1)).timestamp()

        r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)
        print(r.status_code)
        
        for result in r.json()['results']:
            writer.writerow([result[column_name] for column_name in column_names])

        begin_date += timedelta(days=1)


# total_pages = r.json()['total_pages']
# print(r.json()['total_results'])

# r = requests.get(
#     'https://api.buzzsumo.com/search/articles.json', 
#     params={**params, 'page': total_pages - 1}
# )
# data = r.json()

# print(
#     # data['results'][-1]['domain_name'],
#     # data['results'][-1]['url'], 
#     datetime.fromtimestamp(data['results'][-1]['published_date'])
# )
