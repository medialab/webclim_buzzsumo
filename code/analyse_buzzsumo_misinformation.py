import pandas as pd
import numpy as np


df_nb = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_nb.csv')
df_nb['article_number_collected'] = df_nb['article_number'].apply(lambda x: np.min([x, 100]))
print(np.sum(df_nb['article_number_collected']))

# ['domain_name', 'date', 'article_number']
# ['date', 'url', 'published_date', 'domain_name', 'total_shares',
#    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
#    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
#    'facebook_comments', 'facebook_shares']
df1 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_1.csv')
df2 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_2.csv')
df3 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_3.csv')
df4 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_4.csv')
df5 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_5.csv')
df6 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_6.csv')
df7 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_7.csv')
df8 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_8.csv')

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])
print(df.columns)
print(len(df))

# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values(by=['domain_name', 'date'])
# print(np.mean(df['article_number']))
# print(len(df))
# print(df.domain_name.nunique())
# for domain_name in df.domain_name.unique():
#     df_temp = df[df['domain_name']==domain_name]
#     print(domain_name, ': ', len(df_temp), ', ', len(df_temp[df_temp.duplicated(['date'])]))

# df.to_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23.csv', index=False)
