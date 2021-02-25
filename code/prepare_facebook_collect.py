import os
from datetime import datetime, timedelta

import pandas as pd 


domain_name = 'nypost.com'

file_name = "established_news_2021-02-01.csv"
data_path = os.path.join(".", "data", "buzzsumo_domain_name", file_name)
df = pd.read_csv(data_path)

temp_df = df[df['domain_name']==domain_name]
temp_df = temp_df[['url']]
data_path = os.path.join(".", "data", "buzzsumo_domain_name", domain_name.split('.')[0] + '.csv')
temp_df.to_csv(data_path, index=False)