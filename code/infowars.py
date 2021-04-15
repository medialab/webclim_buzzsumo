import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
import ural

from utils import import_data, save_figure


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
    ct_df = ct_df[ct_df['date'] < np.datetime64('2021-01-01')]

    ct_df['link'] = ct_df['link'].apply(lambda x: ural.normalize_url(str(x).strip()))
    ct_df['domain_name'] = ct_df['link'].astype(str).apply(lambda x: ural.get_domain_name(x))
    ct_df = ct_df[ct_df['domain_name']=='infowars.com']

    return ct_df[['date', 'link', 'reaction', 'share', 'comment', 'total_interaction', 'account_name', 'year_month', 'post_url']]


def arrange_plot(ax):

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2017-12-31', '%Y-%m-%d')), 
        np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d'))
    )

    plt.xticks(
        [np.datetime64('2018-06-30'), np.datetime64('2019-06-30'), np.datetime64('2020-06-30')],
        ['2018', '2019', '2020'], fontsize='large'
    )
    ax.xaxis.set_tick_params(length=0)
    plt.axvspan(np.datetime64('2018-01-01'), np.datetime64('2018-12-31'), 
                ymin=0, ymax=200000, facecolor='k', alpha=0.05)
    plt.axvspan(np.datetime64('2020-01-01'), np.datetime64('2020-12-31'), 
                ymin=0, ymax=200000, facecolor='k', alpha=0.05)


def plot_figure_1(ct_df):

    plt.figure(figsize=(10, 5))
    ax = plt.subplot(111)
    plt.title('Engagement for the Facebook public posts sharing an Infowars link', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(ct_df.resample('W', on='date')['reaction'].sum(), label="Reactions (likes, ...) per week")
    plt.plot(ct_df.resample('W', on='date')['share'].sum(), label="Shares per week")
    plt.plot(ct_df.resample('W', on='date')['comment'].sum(), label="Comments per week")
    plt.legend()

    plt.ylim([0, 12500])
    for date in ["2018-08-06", "2019-02-05", "2019-05-02"]:
        plt.plot([np.datetime64(date), np.datetime64(date)], [0, 11000], color='C3', linestyle='-.')
        plt.text(np.datetime64(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=5)), 
                 11100, date, size='medium', color='C3', rotation=30.)

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_1.png')


def print_before_after_statistics(df, begin_date, end_date):

    df_before = df[df['date'] < np.datetime64(begin_date)]
    df_before = df_before[df_before['date'] >= np.datetime64(datetime.strptime(begin_date, '%Y-%m-%d') - timedelta(days=15))]

    df_after = df[df['date'] > np.datetime64(end_date)]
    df_after = df_after[df_after['date'] <= np.datetime64(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=15))]

    print('The total engagement has evolved by',
        int((df_after['total_interaction'].sum() - df_before['total_interaction'].sum()) * 100 / 
            df_before['total_interaction'].sum()), 
        '%. between before', begin_date, 'and after', end_date
    )


def print_2018_vs_2020_statistics(df):

    df_before = df[df['date'] <= np.datetime64('2018-06-30')]
    df_after = df[df['date'] >= np.datetime64('2020-07-01')]

    print('The total engagement has evolved by',
        int((df_after['total_interaction'].sum() - df_before['total_interaction'].sum()) * 100 / 
            df_before['total_interaction'].sum()), 
        '%. between the first 6 months of 2018 and the last 6 months of 2020'
    )


def clean_bz_data(bz_df):

    bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    bz_df['date'] = pd.to_datetime(bz_df['date'])
    bz_df = bz_df[bz_df['date'] > np.datetime64('2017-12-31')]
    bz_df = bz_df[bz_df['date'] < np.datetime64('2021-01-01')]

    bz_df = bz_df.drop_duplicates(subset=['url'])

    return bz_df[['url', 'date', 'total_facebook_shares', 'facebook_likes', 'facebook_shares', 'facebook_comments']]


def plot_supplementary_figure_1(bz_df, ct_df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)
    arrange_plot(ax)

    temp = ct_df[['date', 'link']].sort_values(by=['date']).drop_duplicates(subset=['link'], keep='first')
    plt.plot(temp.resample('D', on='date')['date'].agg('count'), 
        label= "CrowdTangle API", color='C4')

    plt.plot(bz_df.resample('D', on='date')['date'].agg('count'), 
        label= "Buzzsumo API", color='C7')

    plt.legend()
    plt.ylim([0, 80])
    plt.ylabel("Infowars articles published per day")
    save_figure('infowars_supplementary_figure_1.png')


def plot_figure_2(bz_df):

    temp = bz_df[bz_df['date'] < np.datetime64('2020-06-11')]

    plt.figure(figsize=(10, 5))
    ax = plt.subplot(111)
    plt.title('Facebook engagement for the Infowars articles', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(temp.resample('W', on='date')['facebook_likes'].sum(), label="Reactions (likes, ...) per week")
    plt.plot(temp.resample('W', on='date')['facebook_shares'].sum(), label="Shares per week")
    plt.plot(temp.resample('W', on='date')['facebook_comments'].sum(), label="Comments per week")
    plt.legend()

    plt.ylim([0, 180000])
    for date in ["2018-08-06", "2019-02-05", "2019-05-02"]:
        plt.plot([np.datetime64(date), np.datetime64(date)], [0, 158000], color='C3', linestyle='-.')
        plt.text(np.datetime64(date), 160000, date, size='medium', color='C3', rotation=30.)

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_2.png')


def plot_top_spreaders(ct_df, top=10):

    s = ct_df.groupby('account_name')['total_interaction'].sum()
    s = s/np.sum(s)
    s = s.sort_values(ascending=False)[:top]
    list_accounts_to_watch = s.index.values

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

    ct_df = import_data(folder='crowdtangle_domain_name', file_name='infowars_posts.csv')
    ct_df = clean_ct_data(ct_df)
    plot_figure_1(ct_df)

    print_before_after_statistics(ct_df, '2018-07-30', '2018-08-06')
    print_before_after_statistics(ct_df, '2019-02-05', '2019-02-05')
    print_before_after_statistics(ct_df, '2019-05-02', '2019-05-02')
    print_2018_vs_2020_statistics(ct_df)

    bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    bz_df = clean_bz_data(bz_df)
    plot_supplementary_figure_1(bz_df, ct_df)
    plot_figure_2(bz_df)

    # # Illustrate the problematic Buzzsumo crawling patterns:
    # df = import_data(folder='buzzsumo_domain_name', file_name='infowars_nb.csv')
    # print(df.iloc[1257:1268])
    # print(df.iloc[1257:1268].article_number.sum()) 
    # print()
    # print(df.iloc[1372:1461])
    # print(df.iloc[1372:1461].article_number.sum())
    # print()
    # print(df.iloc[365].date)
    # print(df.iloc[1256].date)
    # print(df.iloc[365:1257].article_number.mean())

