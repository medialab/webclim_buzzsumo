from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import save_figure


pd.options.display.max_rows = None


def arrange_plot(ax):

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d') - timedelta(days=4)), 
        np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d') + timedelta(days=4))
    )

    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)


def plot_average_engagement(df):
    
    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title('Average for the {} misinformation domain names'.format(df.domain_name.nunique()), fontsize='x-large')

    arrange_plot(ax)
    plt.plot(df.resample('D', on='date')['facebook_likes'].sum().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook likes per day")
    plt.plot(df.resample('D', on='date')['facebook_shares'].sum().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook shares per day")
    plt.plot(df.resample('D', on='date')['facebook_comments'].sum().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook comments per day")
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df.resample('D', on='date')['twitter_shares'].sum().rolling(window=5, win_type='triang', center=True).mean(), label="Twitter shares per day", color='C3')
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df.resample('D', on='date')['date'].agg('count'), 
        label= "Number of articles published per day", color=[.2, .2, .2])
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='34_misinformation.png')


if __name__=="__main__":

    # ['date', 'url', 'published_date', 'domain_name', 'total_shares',
    #    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
    #    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
    #    'facebook_comments', 'facebook_shares']
    df_url = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23.csv')
    df_url['date'] = [datetime.fromtimestamp(x).date() for x in df_url['published_date']]
    df_url['date'] = pd.to_datetime(df_url['date'])
    plot_average_engagement(df_url)

    # # ['domain_name', 'date', 'article_number']
    # df_nb = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_nb.csv')
    # df_nb['date'] = pd.to_datetime(df_nb['date'])
    # domain_name = "infowars.com"
    # df_nb_temp = df_nb[df_nb['domain_name']==domain_name]

    # plt.figure(figsize=(10, 4))
    # plt.plot(df_nb_temp.resample('D', on='date')['article_number'].sum(), label="Articles published per day")
    # plt.legend()
    # plt.hlines(y=0, color='black', linestyle='--', linewidth=1,
    #            xmin=np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d')), 
    #            xmax=np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d')))
    # plt.show()
