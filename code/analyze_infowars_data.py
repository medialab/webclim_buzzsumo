import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
import ural

from utils import import_data, save_figure


def clean_bz_data(bz_df):

    bz_df['reaction'] = bz_df["facebook_likes"].astype(int)
    bz_df['share'] = bz_df["facebook_shares"].astype(int)
    bz_df['comment'] = bz_df["facebook_comments"].astype(int)
    bz_df['total_interaction'] = bz_df["total_facebook_shares"].astype(int)

    bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    bz_df['date'] = pd.to_datetime(bz_df['date'])
    bz_df = bz_df[bz_df['date'] > np.datetime64('2017-12-31')]

    bz_df = bz_df.drop_duplicates(subset=['url'])

    return bz_df[['url', 'date', 'total_interaction', 'reaction', 'share', 'comment', 'twitter_shares']]


def clean_ct_data(ct_df):

    ct_df['year_month'] = ct_df['date'].apply(lambda x: '-'.join(x.split('-')[:2]))
    ct_df['date'] = pd.to_datetime(ct_df['date'])

    ct_df['account_name'] = ct_df['account_name'].astype(str)

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

    ct_df = ct_df[ct_df['date'] > np.datetime64('2017-12-31')]
    ct_df = ct_df[ct_df['date'] < np.datetime64('2021-03-01')]

    return ct_df[['date', 'link', 'reaction', 'share', 'comment', 'total_interaction', 'account_name', 'year_month']]


def clean_mc_data(mc_df):

    mc_df['date'] = pd.to_datetime(mc_df['publish_date'])
    mc_df = mc_df[mc_df['date'] > np.datetime64('2017-12-31')]
    mc_df = mc_df[mc_df['date'] < np.datetime64('2021-03-01')]

    return mc_df[['url', 'date']]


def arrange_plot(ax):

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2017-12-31', '%Y-%m-%d') - timedelta(days=4)), 
        np.datetime64(datetime.strptime('2021-03-01', '%Y-%m-%d') + timedelta(days=4))
    )

    for date in ["2018-08-01", "2019-02-05", "2019-05-02"]:
        plt.axvline(x=np.datetime64(date), color='black', linestyle='--', linewidth=1)


def plot_engagement(df, platform):

    item = {
        'Buzzsumo': 'article',
        'CrowdTangle': 'post'
    }

    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title('infowars.com data from the ' + platform + ' API', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['reaction'].sum(), label="Likes per week")
    plt.plot(df.resample('W', on='date')['share'].sum(), label="Shares per week")
    plt.plot(df.resample('W', on='date')['comment'].sum(), label="Comments per week")
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['date'].agg('count'), 
        label= item[platform].capitalize() + "s per week", color=[.2, .2, .2])
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['reaction'].mean(), label="Likes per " + item[platform])
    plt.plot(df.resample('W', on='date')['share'].mean(), label="Shares per " + item[platform])
    plt.plot(df.resample('W', on='date')['comment'].mean(), label="Comments per " + item[platform])
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='infowars_' + platform.lower() + '.png')


def plot_buzzsumo_twitter_data(df):

    plt.figure(figsize=(10, 8))

    ax = plt.subplot(211)
    plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['twitter_shares'].sum(),
        label="Twitter shares per week", color='C3')
    plt.legend()

    ax = plt.subplot(212)
    arrange_plot(ax)
    plt.plot(df.resample('W', on='date')['twitter_shares'].mean(),
        label="Twitter shares per article", color='C3')
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='infowars_buzzsumo_twitter.png')


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


def filter_ct_data(ct_df):

    ct_df['link'] = ct_df['link'].apply(lambda x: ural.normalize_url(str(x).strip()))
    ct_df['domain_name'] = ct_df['link'].apply(lambda x: ural.get_domain_name(x))
    ct_df = ct_df[ct_df['domain_name']=='infowars.com']
    ct_df = ct_df[['date', 'link']].sort_values(by=['date'])
    ct_df = ct_df.drop_duplicates(subset=['link'], keep='first')

    return ct_df


def plot_daily_article_number(bz_df, mc_df, ct_df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)
    arrange_plot(ax)

    plt.plot(bz_df.resample('W', on='date')['date'].agg('count'), 
        label= "Buzzsumo (" + str(bz_df.url.nunique()) + " articles)", color=[.2, .2, .2])
    plt.plot(mc_df.resample('W', on='date')['date'].agg('count'), 
        label= "Media Cloud (" + str(mc_df.url.nunique()) + " articles)", color='C3')
    plt.plot(ct_df.resample('W', on='date')['date'].agg('count'), 
        label= "CrowdTangle (" + str(ct_df.link.nunique()) + " articles)", color='C4')
    plt.legend()

    plt.ylabel("Articles per week")
    save_figure('infowars_article_number.png')


if __name__=="__main__":

    bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    bz_df = clean_bz_data(bz_df)
    # plot_engagement(bz_df, platform="Buzzsumo")
    # plot_buzzsumo_twitter_data(bz_df)

    ct_df = import_data(folder='crowdtangle_domain_name', file_name='infowars_posts.csv')
    ct_df = clean_ct_data(ct_df)
    # plot_engagement(ct_df, platform="CrowdTangle")
    # plot_top_spreaders(ct_df, top=10)

    mc_df = import_data(folder='mediacloud', file_name='infowars.csv')
    mc_df = clean_mc_data(mc_df)
    ct_df = filter_ct_data(ct_df)
    plot_daily_article_number(bz_df, mc_df, ct_df)
