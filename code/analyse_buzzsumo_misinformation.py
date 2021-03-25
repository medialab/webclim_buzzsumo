from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from plot_buzzsumo_data import plot_platform_metrics


pd.options.display.max_rows = None


if __name__=="__main__":

    # ['domain_name', 'date', 'article_number']
    df_nb = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_nb.csv')
    df_nb['date'] = pd.to_datetime(df_nb['date'])
    domain_name = "infowars.com"
    df_nb_temp = df_nb[df_nb['domain_name']==domain_name]

    # plt.figure(figsize=(10, 4))
    # plt.title(domain_name)
    # plt.plot(df_nb_temp.resample('D', on='date')['article_number'].sum(), label="Articles published per day")
    # plt.legend()
    # plt.show()

    # ['date', 'url', 'published_date', 'domain_name', 'total_shares',
    #    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
    #    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
    #    'facebook_comments', 'facebook_shares']
    df_url = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23.csv')
    print(len(df_url))
    df_url['date'] = [datetime.fromtimestamp(x).date() for x in df_url['published_date']]
    df_url['date'] = pd.to_datetime(df_url['date'])

    # plt.figure(figsize=(10, 12))
    # ax = plt.subplot(311)
    # plot_platform_metrics(df_url)
    # plt.show()
