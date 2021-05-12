import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import import_data


def rolling_average(df, column):
    return df.groupby(by=["date"])[column].mean().rolling(window=7, win_type='triang', center=True).mean()


def arrange_figure(ax):

    plt.legend()

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d') - timedelta(days=4)), 
        np.datetime64(datetime.strptime('2021-05-01', '%Y-%m-%d') + timedelta(days=4))
    )
    plt.ylim(bottom=0)


def save_main_figure(domain_name=None):
    if domain_name:
        figure_name = domain_name + '.png'
    else:
        figure_name = 'global.png'
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))


def plot_platform_metrics(df, domain_name=None):

    plt.figure(figsize=(10, 8))

    ax = plt.subplot(3, 1, 1)
    plt.plot(rolling_average(df, 'facebook_likes'), label="Facebook reactions per article", color="C0")
    plt.plot(rolling_average(df, 'facebook_shares'), label="Facebook shares per article", color="C1")
    plt.plot(rolling_average(df, 'facebook_comments'), label="Facebook comments per article", color="C2")
    arrange_figure(ax)

    if domain_name:
        plt.title(domain_name, fontsize='x-large')
    else:
        plt.title('Misinformation domain names', fontsize='x-large')
    
    ax = plt.subplot(3, 1, 2)
    plt.plot(rolling_average(df, 'twitter_shares'), label="Twitter shares per article", color="C3")
    arrange_figure(ax)

    ax = plt.subplot(3, 1, 3)
    plt.plot(df["date"].value_counts().sort_index().rolling(window=7, win_type='triang', center=True).mean(), 
        label="Articles per day", color=[.2, .2, .2])
    arrange_figure(ax)

    plt.tight_layout()
    if domain_name:
        save_main_figure(domain_name.split('.')[0])
    else:
        save_main_figure()


if __name__=="__main__":

    # df = import_data(folder='buzzsumo_domain_name', file_name='lifesitenews.csv')
    df = import_data(folder='buzzsumo_domain_name', file_name='thebl.csv')

    df['date'] = [datetime.fromtimestamp(x).date() for x in df['published_date']]
    df['date'] = pd.to_datetime(df['date'])

    plot_platform_metrics(df)

    for domain_name in df['domain_name'].unique():
        temp_df = df[df['domain_name']==domain_name]
        plot_platform_metrics(temp_df, domain_name)


