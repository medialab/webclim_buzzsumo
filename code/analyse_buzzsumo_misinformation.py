from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import save_figure


# pd.options.display.max_rows = None


def import_buzzsumo_data():

    df_url_1 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23.csv')
    df_url_2 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-30.csv')
    df_url = pd.concat([df_url_1, df_url_2])

    df_url['date'] = [datetime.fromtimestamp(x).date() for x in df_url['published_date']]
    df_url['date'] = pd.to_datetime(df_url['date'])
    df_url = df_url.drop_duplicates(subset=['url'])

    return df_url


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


def rolling_average(df, column):
    return df.resample('D', on='date')[column].mean().rolling(window=7, win_type='triang', center=True).mean()


def plot_one_domain(df_url, domain_name):

    df_url_domain = df_url[df_url['domain_name']==domain_name]

    plt.plot(rolling_average(df_url_domain, 'facebook_likes'), label="Reactions per article", color="C0")
    plt.plot(rolling_average(df_url_domain, 'facebook_shares'), label="Shares per article", color="C1")
    plt.plot(rolling_average(df_url_domain, 'facebook_comments'), label="Comments per article", color="C2")


def plot_figure_1(df_url):

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 5)
    ax = fig.add_subplot(gs[0, :])

    domain_name = 'breitbart.com'
    plot_one_domain(df_url, domain_name)
    plt.legend()
    arrange_plot(ax)
    plt.title("Engagement metrics for one 'repeat offender' domain name (" + domain_name + ")")
    
    plt.tight_layout()
    save_figure(figure_name='figure_1.png')


def plot_figure_2(df_url):
    
    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title("Average for the {} 'repeat offender' domain names".format(df_url.domain_name.nunique()), fontsize='x-large')

    arrange_plot(ax)
    plt.plot(df_url.groupby(by=["date"])["facebook_likes"].sum()/df_url.groupby(by=["date"])["domain_name"].nunique(), 
            label="Reactions per day", color="C0")
    plt.plot(df_url.groupby(by=["date"])["facebook_shares"].sum()/df_url.groupby(by=["date"])["domain_name"].nunique(), 
            label="Shares per day", color="C1")
    plt.plot(df_url.groupby(by=["date"])["facebook_comments"].sum()/df_url.groupby(by=["date"])["domain_name"].nunique(), 
            label="Comments per day", color="C2")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.ylim(0, 130000)
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df_url["date"].value_counts().sort_index()/df_url.groupby(by=["date"])["domain_name"].nunique(), 
        label="Articles per day", color=[.2, .2, .2])
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df_url.groupby(by=["date"])["facebook_likes"].sum()/df_url["date"].value_counts().sort_index(), 
            label="Reactions per article")
    plt.plot(df_url.groupby(by=["date"])["facebook_shares"].sum()/df_url["date"].value_counts().sort_index(), 
            label="Shares per article")
    plt.plot(df_url.groupby(by=["date"])["facebook_comments"].sum()/df_url["date"].value_counts().sort_index(), 
            label="Comments per article")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.ylim(0, 6500)
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='figure_2.png')


def plot_figure_3(df_url):

    domains_to_plot = [
        'foxnews.com',
        'americanthinker.com',
        'thelibertybeacon.com',
        'theepochtimes.com',
        'gellerreport.com',
        # 'breitbart.com',
        'newspunch.com',
        'therightscoop.com',
        'wnd.com',
        'thegatewaypundit.com',
        'theblaze.com',
    ]

    fig = plt.figure(figsize=(10, 12))

    for idx in range(len(domains_to_plot)):

        ax = plt.subplot(5, 2, idx + 1)

        plot_one_domain(df_url, domains_to_plot[idx])
        if idx == 0:
            plt.legend()
        arrange_plot(ax)
        plt.title(domains_to_plot[idx])

        xticks = [np.datetime64('2019-01-01'), np.datetime64('2019-05-01'), np.datetime64('2019-09-01'),
                np.datetime64('2020-01-01'), np.datetime64('2020-05-01'), np.datetime64('2020-09-01')
                ]
        plt.xticks(xticks, rotation=30, ha='right')

    plt.tight_layout()
    save_figure('figure_3.png')


if __name__=="__main__":

    # ['date', 'url', 'published_date', 'domain_name', 'total_shares',
    #    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
    #    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
    #    'facebook_comments', 'facebook_shares']
    df_url = import_buzzsumo_data()

    plot_figure_1(df_url)
    plot_figure_2(df_url)
    plot_figure_3(df_url)
