import pandas as pd


df_url = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-30.csv')
print(len(df_url))
df_url = df_url.drop_duplicates(subset=['url'])
print(len(df_url))

print(df_url.domain_name.unique())
print(df_url.domain_name.nunique())
print()

df_nb = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-30_nb.csv')
print(46 * 731)
print(len(df_nb))
print(df_nb.domain_name.unique())
print(df_nb.domain_name.nunique())
