from datetime import datetime, timedelta

import pandas as pd
import numpy as np


df1 = pd.read_csv('./data/buzzsumo_domain_name/principia_2021-02-24.csv')
df2 = pd.read_csv('./data/buzzsumo_domain_name/health_2021-02-24.csv')
df3 = pd.read_csv('./data/buzzsumo_domain_name/misinfo_news_2021-02-24.csv')
df4 = pd.read_csv('./data/buzzsumo_domain_name/misinfo_news_infowars_2021-02-23.csv')
df5 = pd.read_csv('./data/buzzsumo_domain_name/sott_2021-02-24.csv')

print(len(df1) + len(df2) + len(df3) + len(df4) + len(df5))

print()

df = pd.concat([df1, df2, df3, df4, df5])
print(len(df))
print(df['domain_name'].unique())

df.to_csv('./data/buzzsumo_domain_name/misinfo_news_2021-02-23.csv', index=False)