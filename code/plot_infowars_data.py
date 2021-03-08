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

    columns_to_plot = [
        "total_facebook_shares",
        "twitter_shares"
    ]

    plt.figure(figsize=(10, 7))

    for subplot_index in range(2):

        ax = plt.subplot(2, 1, subplot_index + 1)

        plt.plot(df.groupby(by=["date"])[columns_to_plot[subplot_index]].sum(),
                label=columns_to_plot[subplot_index], color='C' + str(subplot_index))
        plt.legend()

        arrange_plot(ax)

        if subplot_index == 0:
            plt.axvline(x=np.datetime64("2018-08-01"), color='black', linestyle='--', linewidth=1)
            plt.axvline(x=np.datetime64("2019-02-05"), color='black', linestyle='--', linewidth=1)
            plt.axvline(x=np.datetime64("2019-05-02"), color='black', linestyle='--', linewidth=1)
        elif subplot_index == 1:
            plt.axvline(x=np.datetime64("2019-05-02"), color='black', linestyle='--', linewidth=1)

        if subplot_index == 0:
            plt.title('infowars.com data from the Buzzsumo API', fontsize='x-large')
            plt.ylim(top=100000)
        elif subplot_index == 1:
            plt.ylim(top=20000)

    plt.tight_layout()

    save_figure(figure_name='infowars_buzzsumo.png')


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


if __name__=="__main__":

    bz_df = import_data(folder='buzzsumo_domain_name', file_name='infowars.csv')
    bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]
    plot_buzzsumo_data(bz_df)

    ct_df = import_data(folder='crowdtangle_domain_name', file_name='infowars_posts.csv')
    ct_df = clean_ct_data(ct_df)
    plot_crowdtangle_data(ct_df)
