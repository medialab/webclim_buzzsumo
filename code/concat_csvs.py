from datetime import datetime, timedelta

import pandas as pd
import numpy as np


df1 = pd.read_csv('./data/buzzsumo_domain_name/articles.csv')
df2 = pd.read_csv('./data/buzzsumo_domain_name/articles_2.csv')
df3 = pd.read_csv('./data/buzzsumo_domain_name/articles_3.csv')
df4 = pd.read_csv('./data/buzzsumo_domain_name/articles_4.csv')

print(len(df1) + len(df2) + len(df3) + len(df4))

print()

df = pd.concat([df1, df2, df3, df4])
print(len(df))

df.to_csv('./data/buzzsumo_domain_name/misinfo_news_infowars.csv', index=False)