import os

import pandas as pd 


# domain_name = "breitbart.com"
# file_name = 'misinfo_news_2021-02-24.csv'

domain_name = "nypost.com"
file_name = 'established_news_2021-02-01.csv'

input_path = os.path.join('.', 'data', 'buzzsumo_domain_name', file_name)
df = pd.read_csv(input_path)

df = df[df['domain_name'] == domain_name]
df = df.iloc[:1000]
print(len(df))

output_name = domain_name.split('.')[0] + '.csv'
output_path = os.path.join('.', 'data', 'buzzsumo_domain_name', output_name)

df.to_csv(output_path, index=False)