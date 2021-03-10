import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz

from utils import import_data, save_figure


def arrange_plot(ax):

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2016-12-31', '%Y-%m-%d') - timedelta(days=4)), 
        np.datetime64(datetime.strptime('2021-03-01', '%Y-%m-%d') + timedelta(days=4))
    )
    plt.ylim(bottom=0)


def plot_buzzsumo_data(df):

    ## Facebook data
    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)

    plt.plot(df.groupby(by=["date"])["total_facebook_shares"].sum(),
            label="total_facebook_interaction", color='C0')
    plt.legend()
    arrange_plot(ax)

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')
    plt.ylim(top=100000)

    plt.tight_layout()
    save_figure(figure_name='infowars_buzzsumo_facebook.png')

    ## Twitter data
    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)

    plt.plot(df.groupby(by=["date"])["twitter_shares"].sum(),
        label="twitter_shares", color='C1')
    plt.legend()
    arrange_plot(ax)

    plt.axvline(x=np.datetime64("2019-09-01"), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')
    plt.ylim(top=20000) 

    plt.tight_layout()
    save_figure(figure_name='infowars_buzzsumo_twitter.png')


def clean_ct_data(ct_df):

    ct_df['date'] = pd.to_datetime(ct_df['date'])

    # ct_df['account_name'] = ct_df['account_name'].astype(str)
    # ct_df['account_id'] = ct_df['account_id'].astype(int)

    ct_df['total_interaction'] = ct_df[[
        "actual_share_count", "actual_comment_count",
        "actual_like_count", "actual_favorite_count", "actual_love_count",
        "actual_wow_count", "actual_haha_count", "actual_sad_count",
        "actual_angry_count", "actual_thankful_count", "actual_care_count"
    ]].sum(axis=1).astype(int)

    return ct_df[['date', 'total_interaction']]


def plot_crowdtangle_data(df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)

    plt.plot(df.groupby(by=['date'])['total_interaction'].sum(),
             label='total_facebook_interaction')
    plt.legend()
    arrange_plot(ax)

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the CrowdTangle API', fontsize='x-large')
    plt.ylim(top=20000)

    plt.tight_layout()
    save_figure(figure_name='infowars_crowdtangle.png')


def plot_facebook_like_data(df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)

    plt.plot(df.groupby(by=['date'])['approx_likes_int'].sum(),
             label='total_facebook_interaction')
    plt.legend()

    arrange_plot(ax)

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the Facebook Like button plugin', fontsize='x-large')
    plt.ylim(top=150000)

    plt.tight_layout()
    save_figure(figure_name='infowars_facebook_like.png')


def plot_article_number(df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)
    plt.plot(df['date'], df['article_number'], label='Buzzsumo')
    plt.legend()
    arrange_plot(ax)

    plt.ylim([0, 100])

    plt.tight_layout()
    plt.show()


if __name__=="__main__":

    # bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    # bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    # plot_buzzsumo_data(bz_df)

    # ct_df = import_data(folder='crowdtangle_domain_name', file_name='infowars_posts.csv')
    # ct_df = clean_ct_data(ct_df)
    # plot_crowdtangle_data(ct_df)

    # fl_df = import_data(folder='facebook_url_like', file_name='infowars.csv')
    # fl_df = fl_df.dropna(subset=['approx_likes_int'])
    # fl_df['date'] = [datetime.fromtimestamp(x).date() for x in fl_df['published_date']]
    # plot_facebook_like_data(fl_df)

    bz_nb_df = import_data(folder='buzzsumo_domain_name', file_name='infowars_nb.csv')
    bz_nb_df['date'] = pd.to_datetime(bz_nb_df['date'])
    print(len(bz_nb_df))
    print(np.min(bz_nb_df['date']), np.max(bz_nb_df['date']))
    plot_article_number(bz_nb_df)

