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


def plot_facebook_engagement(df_temp):
    plt.plot(df_temp.resample('D', on='date')['facebook_likes'].mean().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook likes per post")
    plt.plot(df_temp.resample('D', on='date')['facebook_shares'].mean().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook shares per post")
    plt.plot(df_temp.resample('D', on='date')['facebook_comments'].mean().rolling(window=5, win_type='triang', center=True).mean(), label="Facebook comments per post")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)


def plot_average_engagement(df):
    
    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title('Average for the {} misinformation domain names'.format(df.domain_name.nunique()), fontsize='x-large')

    arrange_plot(ax)
    plot_facebook_engagement(df)
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df.resample('D', on='date')['twitter_shares'].mean().rolling(window=5, win_type='triang', center=True).mean(), label="Twitter shares per tweet", color='C3')
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df.resample('D', on='date')['date'].agg('count'), 
        label="Sum of articles published per day", color=[.2, .2, .2])
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='{}_misinformation_engagement.png'.format(df.domain_name.nunique()))


def compute_normalized_average(df, column):
    df_temp = pd.DataFrame()
    for domain_name in df.domain_name.unique():
        s_temp = df[df['domain_name']==domain_name].resample('D', on='date')[column].mean()
        df_temp[domain_name] = (s_temp - s_temp.mean()) / s_temp.std()
    return df_temp.mean(axis=1)


def plot_normalized_average(df):

    plt.figure(figsize=(10, 8))

    ax = plt.subplot(211)
    plt.title('Normalized average for the {} misinformation domain names'.format(df.domain_name.nunique()), fontsize='x-large')

    arrange_plot(ax)
    for column in ['facebook_likes', 'facebook_shares', 'facebook_comments']:
        plt.plot(compute_normalized_average(df, column).rolling(window=5, win_type='triang', center=True).mean(), 
                label="Facebook " + column.split('_')[1] + " per post")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.legend()

    ax = plt.subplot(212)
    arrange_plot(ax)
    plt.plot(compute_normalized_average(df, 'twitter_shares').rolling(window=5, win_type='triang', center=True).mean(), 
             label="Twitter shares per tweet", color='C3')
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='{}_normalized_average.png'.format(df.domain_name.nunique()))


def plot_individual_engagement(df_url):

    domain_name_index = 0    
    for domain_name in df_url.domain_name.unique():

        if domain_name_index % 10 == 0:
            plt.figure(figsize=(12, 14))

        ax = plt.subplot(5, 2, domain_name_index % 10 + 1)
        arrange_plot(ax)
        plot_facebook_engagement(df_url[df_url['domain_name']==domain_name])
        if domain_name_index % 10 == 0: plt.legend()
        plt.title(domain_name)

        if (domain_name_index % 10 == 9) | (domain_name_index == df_url.domain_name.nunique() - 1):
            plt.tight_layout()
            save_figure('{}_misinformation_engagement_{}.png'.format(df_url.domain_name.nunique(), int(domain_name_index / 10) + 1))

        domain_name_index += 1


def plot_article_number_individually(df_nb):

    domain_name_index = 0    
    for domain_name in df_nb.domain_name.unique():

        if domain_name_index % 10 == 0:
            plt.figure(figsize=(12, 14))

        ax = plt.subplot(5, 2, domain_name_index % 10 + 1)

        plt.plot(df_nb[df_nb['domain_name']==domain_name].resample('D', on='date')['article_number'].sum(), 
                 label="Number of articles published per day", color=[.2, .2, .2])
        plt.hlines(y=0, color='black', linestyle='--', linewidth=1,
                xmin=np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d')), 
                xmax=np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d')))
        arrange_plot(ax)
        if domain_name_index % 10 == 0: plt.legend()
        plt.title(domain_name)

        if (domain_name_index % 10 == 9) | (domain_name_index == df_nb.domain_name.nunique() - 1):
            plt.tight_layout()
            save_figure('{}_misinformation_article_nb_{}.png'.format(df_nb.domain_name.nunique(), int(domain_name_index / 10) + 1))

        domain_name_index += 1


if __name__=="__main__":

    # ['date', 'url', 'published_date', 'domain_name', 'total_shares',
    #    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
    #    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
    #    'facebook_comments', 'facebook_shares']
    df_url_1 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23.csv')
    df_url_2 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-30.csv')
    df_url = pd.concat([df_url_1, df_url_2])

    df_url['date'] = [datetime.fromtimestamp(x).date() for x in df_url['published_date']]
    df_url['date'] = pd.to_datetime(df_url['date'])
    df_url = df_url.drop_duplicates(subset=['url'])
    plot_average_engagement(df_url)
    plot_normalized_average(df_url)

    # plot_individual_engagement(df_url)

    # excluded_domain_name = ['zerohedge.com', 'stateofthenation.co', 'principia-scientific.com', 'newsbreak.com', 'infowars.com', 'humansarefree.com', 'greenmedinfo.com', 'dcdirtylaundry.com', 'dcclothesline.com', 'davidicke.com']
    # df_url = df_url[~df_url['domain_name'].isin(excluded_domain_name)]
    # plot_average_engagement(df_url)
    # save_figure(figure_name='34_misinformation_engagement_filtered.png')

    # # ['domain_name', 'date', 'article_number']
    # df_nb_1 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-23_nb.csv')
    # df_nb_2 = pd.read_csv('./data/buzzsumo_domain_name/misinformation_2021-03-30_nb.csv')
    # df_nb = pd.concat([df_nb_1, df_nb_2])

    # df_nb['date'] = pd.to_datetime(df_nb['date'])
    # plot_article_number_individually(df_nb)