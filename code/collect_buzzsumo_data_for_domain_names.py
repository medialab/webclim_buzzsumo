import os
from datetime import datetime
import csv

from dotenv import load_dotenv
import requests


# NBC, The Daily Mail, CNN, Fox News, The Independent, BBC, The New York Times, The Washington Post, Yahoo and The New York Post

load_dotenv()
BUZZSUMO_API_KEY = os.getenv('BUZZSUMO_API_KEY')

# domain_name_example = 'nytimes.com'
domain_name_example = 'cnn.com'

params = {
    'q': domain_name_example,
    'api_key': BUZZSUMO_API_KEY,
    'num_results': 100,
    'begin_date': datetime.timestamp(datetime.strptime('2019-01-01', '%Y-%m-%d')),
    'end_date': datetime.timestamp(datetime.strptime('2019-01-02', '%Y-%m-%d'))
}
r = requests.get('https://api.buzzsumo.com/search/articles.json', params=params)
print(r.status_code)

column_names = [
    'url',
    'date',
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
    
    for result in r.json()['results']:
        row_to_add = [
            result['url'],
            datetime.fromtimestamp(result['published_date']),
            result['domain_name'], 
            result['total_shares'],
            result['alexa_rank'],
            result['pinterest_shares'],
            result['total_reddit_engagements'], 
            result['twitter_shares'],
            result['total_facebook_shares'],
            result['facebook_likes'],
            result['facebook_comments'],
            result['facebook_shares']
        ]
        writer.writerow(row_to_add)

total_pages = r.json()['total_pages']
print(r.json()['total_results'])

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
