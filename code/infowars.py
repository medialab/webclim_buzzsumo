import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
import ural
from wordcloud import WordCloud, STOPWORDS

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

    return ct_df[['date', 'link', 'reaction', 'share', 'comment', 'total_interaction', 'account_name', 'year_month', 'post_url', 'message']]


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


def calculate_rolling_sum(df, column):
    return df.resample('D', on='date')[column].sum().rolling(window=14, win_type='triang', center=True).mean()


def plot_figure_1(ct_df):

    plt.figure(figsize=(10, 5))
    ax = plt.subplot(111)
    plt.title('Engagement for the Facebook public posts sharing an Infowars link (CrowdTangle)', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(calculate_rolling_sum(ct_df, 'reaction'), label="Reactions (likes, ...) per day")
    plt.plot(calculate_rolling_sum(ct_df, 'share'), label="Shares per day")
    plt.plot(calculate_rolling_sum(ct_df, 'comment'), label="Comments per day")
    plt.legend()

    plt.ylim([0, 1700])
    for date in ["2018-08-06", "2019-02-05", "2019-05-02"]:
        plt.plot([np.datetime64(date), np.datetime64(date)], [0, 1500], color='C3', linestyle='-.')
        plt.text(np.datetime64(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=5)), 
                 1520, date, size='medium', color='C3', rotation=30.)

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_1.png')


def clean_bz_data(bz_df):

    bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    bz_df['date'] = pd.to_datetime(bz_df['date'])
    bz_df = bz_df[bz_df['date'] > np.datetime64('2017-12-31')]
    bz_df = bz_df[bz_df['date'] < np.datetime64('2021-01-01')]

    bz_df = bz_df.drop_duplicates(subset=['url'])

    bz_df['total_interaction'] = bz_df['total_facebook_shares']

    return bz_df[['url', 'date', 'total_interaction', 'facebook_likes', 'facebook_shares', 'facebook_comments']]


def plot_supplementary_figure_1(bz_df, ct_df):

    plt.figure(figsize=(10, 4))
    ax = plt.subplot(111)
    arrange_plot(ax)

    temp = ct_df[['date', 'link']].sort_values(by=['date']).drop_duplicates(subset=['link'], keep='first')
    plt.plot(temp.resample('D', on='date')['date'].agg('count'), 
        label= "Found in the Facebook posts from the CrowdTangle API", color='C4')

    plt.plot(bz_df.resample('D', on='date')['date'].agg('count'), 
        label= "According to the Buzzsumo API", color='C7')

    plt.legend()
    plt.ylim([0, 80])
    plt.title('Number of Infowars articles published per day', fontsize='x-large')
    save_figure('infowars_supplementary_figure_1.png')


def calculate_and_filter_rolling_sum(df, column):
    s = calculate_rolling_sum(df, column)
    s.loc['2020-06-11':'2020-06-21'] = np.nan
    s.loc['2020-09-01':] = np.nan
    return s


def plot_figure_2(bz_df):

    plt.figure(figsize=(10, 5))
    ax = plt.subplot(111)
    plt.title('Facebook engagement for the Infowars articles (Buzzsumo)', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(calculate_and_filter_rolling_sum(bz_df, 'facebook_likes'), label="Reactions (likes, ...) per day")
    plt.plot(calculate_and_filter_rolling_sum(bz_df, 'facebook_shares'), label="Shares per day")
    plt.plot(calculate_and_filter_rolling_sum(bz_df, 'facebook_comments'), label="Comments per day")
    plt.legend(loc='upper right')

    plt.ylim([0, 24000])
    for date in ["2018-08-06", "2019-02-05", "2019-05-02"]:
        plt.plot([np.datetime64(date), np.datetime64(date)], [0, 21000], color='C3', linestyle='-.')
        plt.text(np.datetime64(date), 21200, date, size='medium', color='C3', rotation=30.)

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_2.png')


def print_before_after_engagement(df, begin_date, end_date, period=60):

    df_before = df[df['date'] < np.datetime64(begin_date)]
    df_before = df_before[df_before['date'] >= np.datetime64(datetime.strptime(begin_date, '%Y-%m-%d') - timedelta(days=period))]

    df_after = df[df['date'] > np.datetime64(end_date)]
    df_after = df_after[df_after['date'] <= np.datetime64(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=period))]

    print('The total engagement has evolved by',
        int((df_after['total_interaction'].sum() - df_before['total_interaction'].sum()) * 100 / 
            df_before['total_interaction'].sum()), 
        '%. between before', begin_date, 'and after', end_date
    )


def plot_figure_4(ct_df):

    stop_words = ["https", "s", "v", "los", "la" "de", "one", "la", "que", "will"] + list(STOPWORDS)
    ct_df_temp = ct_df.dropna(subset=['message'])

    posts_message_before = ' --- '.join(ct_df_temp[ct_df_temp['date'] < np.datetime64('2019-05-02')]['message'].tolist())
    posts_message_after  = ' --- '.join(ct_df_temp[ct_df_temp['date'] > np.datetime64('2019-05-02')]['message'].tolist())

    figure = plt.figure(figsize=(10, 3.3))
    figure.suptitle("Content of the public Facebook posts sharing an Infowars link", fontsize='x-large')
    
    ax = plt.subplot(121)
    ax.set_title('Before May 2, 2019')

    wordcloud = WordCloud(stopwords=stop_words, background_color="white").generate(posts_message_before)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    ax = plt.subplot(122)
    ax.set_title('After May 2, 2019')

    wordcloud = WordCloud(stopwords=stop_words, background_color="white").generate(posts_message_after)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_4.png')


def plot_figure_5(ct_df):

    plt.figure(figsize=(10, 5))
    ax = plt.subplot(111)
    plt.title('Daily number of Facebook public posts sharing an Infowars link (CrowdTangle)', fontsize='x-large')

    arrange_plot(ax)
    plt.plot(ct_df.resample('D', on='date')['date'].agg('count').rolling(window=14, win_type='triang', center=True).mean(), 
             label="Number of Facebook posts per day", color='grey')
    plt.legend(loc='upper right')

    plt.ylim([0, 120])
    for date in ["2018-08-06", "2019-02-05", "2019-05-02"]:
        plt.plot([np.datetime64(date), np.datetime64(date)], [0, 102], color='C3', linestyle='-.')
        plt.text(np.datetime64(date), 105, date, size='medium', color='C3', rotation=30.)

    plt.tight_layout()
    save_figure(figure_name='infowars_figure_5.png')


def print_before_after_post_number(df, begin_date, end_date, period=60):

    df_before = df[df['date'] < np.datetime64(begin_date)]
    df_before = df_before[df_before['date'] >= np.datetime64(datetime.strptime(begin_date, '%Y-%m-%d') - timedelta(days=period))]

    df_after = df[df['date'] > np.datetime64(end_date)]
    df_after = df_after[df_after['date'] <= np.datetime64(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=period))]

    print('The daily number of posts has evolved by',
        int((df_after.resample('D', on='date')['date'].agg('count').sum() - df_before.resample('D', on='date')['date'].agg('count').sum()) * 100 / 
            df_before.resample('D', on='date')['date'].agg('count').sum()), 
        '%. between before', begin_date, 'and after', end_date
    )


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

    bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    bz_df = clean_bz_data(bz_df)
    plot_supplementary_figure_1(bz_df, ct_df)
    plot_figure_2(bz_df)

    print('\n Statistics for CT:')
    print_before_after_engagement(ct_df, '2018-07-30', '2018-08-06')
    print_before_after_engagement(ct_df, '2019-02-05', '2019-02-05')
    print_before_after_engagement(ct_df, '2019-05-02', '2019-05-02')

    print('\n Statistics for BZ:')
    print_before_after_engagement(bz_df, '2018-07-30', '2018-08-06')
    print_before_after_engagement(bz_df, '2019-02-05', '2019-02-05')
    print_before_after_engagement(bz_df, '2019-05-02', '2019-05-02')
    print()

    plot_figure_4(ct_df)
    plot_figure_5(ct_df)
    print_before_after_post_number(ct_df, '2019-05-02', '2019-05-02')

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