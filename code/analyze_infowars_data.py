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

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)


def plot_buzzsumo_data(df):

    ## Facebook data
    arrange_plot()

    plt.plot(df.groupby(by=["date"])["total_facebook_shares"].mean(),
            label="total_facebook_interaction", color='C0')
    plt.legend()

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')

    plt.tight_layout()
    save_figure(figure_name='infowars_buzzsumo_facebook.png')

    ## Twitter data
    arrange_plot()
    plt.plot(df.groupby(by=["date"])["twitter_shares"].sum(),
        label="twitter_shares", color='C1')
    plt.legend()

    plt.axvline(x=np.datetime64("2019-09-01"), color='black', linestyle='--', linewidth=1)
    plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')

    plt.tight_layout()
    save_figure(figure_name='infowars_buzzsumo_twitter.png')


def clean_ct_data(ct_df):

    ct_df['year_month'] = ct_df['date'].apply(lambda x: '-'.join(x.split('-')[:2]))
    ct_df['date'] = pd.to_datetime(ct_df['date'])

    # ct_df['account_name'] = ct_df['account_name'].astype(str)
    # ct_df['account_id'] = ct_df['account_id'].astype(int)

    ct_df['reaction'] = ct_df[[
        "actual_like_count", "actual_favorite_count", "actual_love_count",
        "actual_wow_count", "actual_haha_count", "actual_sad_count",
        "actual_angry_count", "actual_thankful_count", "actual_care_count"
    ]].sum(axis=1).astype(int)
    ct_df['share'] = ct_df["actual_share_count"].astype(int)
    ct_df['comment'] = ct_df["actual_comment_count"].astype(int)

    ct_df['total_interaction'] = ct_df[[
        "reaction", "share", "comment"
    ]].sum(axis=1).astype(int)

    ct_df = ct_df[ct_df['date'] > np.datetime64('2016-12-31')]
    ct_df = ct_df[ct_df['date'] < np.datetime64('2021-03-01')]

    return ct_df[['date', 'reaction', 'share', 'comment', 'total_interaction', 'account_name', 'year_month']]


def plot_crowdtangle_data(df):

    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title('infowars.com data from the CrowdTangle API', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['reaction'].sum(), label="Likes per week")
    plt.plot(df.resample('W', on='date')['share'].sum(), label="Shares per week")
    plt.plot(df.resample('W', on='date')['comment'].sum(), label="Comments per week")
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['date'].agg('count'), 
        label="Posts per week", color=[.2, .2, .2])
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['reaction'].mean(), label="Likes per post")
    plt.plot(df.resample('W', on='date')['share'].mean(), label="Shares per post")
    plt.plot(df.resample('W', on='date')['comment'].mean(), label="Comments per post")
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='infowars_crowdtangle.png')


def plot_top_spreaders(ct_df, top=10):

    s = ct_df.groupby('account_name')['total_interaction'].sum()
    s = s/np.sum(s)
    s = s.sort_values(ascending=False)[:top]
    list_accounts_to_watch = s.index.values
    # print(s)

    table = pd.pivot_table(ct_df, values='total_interaction', aggfunc=np.sum, 
                           index=['year_month'], columns=['account_name'])
    table['total'] = table.sum(axis=1) / 100
    table = table.fillna(0)
    table = table.div(table['total'], axis=0)
    table = table[list_accounts_to_watch]

    table.plot.area()
    plt.xlabel('')
    plt.ylabel('Percentage in Facebook total engagement')
    save_figure('infowars_top' + str(top) + '_spreaders.png')


if __name__=="__main__":

    # bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    # bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    # # bz_df = bz_df[bz_df['date'] > np.datetime64('2017-12-31')]
    # plot_buzzsumo_data(bz_df)

    ct_df = import_data(folder='crowdtangle_domain_name', file_name='infowars_posts.csv')
    ct_df = clean_ct_data(ct_df)
    plot_crowdtangle_data(ct_df)
    # plot_top_spreaders(ct_df)
