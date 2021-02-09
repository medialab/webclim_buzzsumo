import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_platform_metrics(df, domain_name=None):

    columns_to_plot = [
        "total_facebook_shares",
        "twitter_shares",
        "total_reddit_engagements",
        "pinterest_shares",
        "alexa_rank",
    ]

    plt.figure(figsize=(10, 15))

    for subplot_index in range(5):

        ax = plt.subplot(5, 1, subplot_index + 1)

        plt.plot(df.groupby(by=["date"])[columns_to_plot[subplot_index]].mean(),
                label=columns_to_plot[subplot_index], color='C' + str(subplot_index))
        plt.legend()

        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.grid(axis="y")
        plt.locator_params(axis='y', nbins=4)

        plt.xlim(
            np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d') - timedelta(days=4)), 
            np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d') + timedelta(days=4))
        )
        plt.ylim(bottom=0)

        if subplot_index == 0:
            if domain_name:
                plt.title(domain_name, fontsize='x-large')
            else:
                plt.title('Established news domain names', fontsize='x-large')

    plt.tight_layout()


def save_main_figure(domain_name=None):
    figure_name = 'established_news.png'
    if domain_name:
        figure_name = 'established_news_' + domain_name + '.png'
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))


if __name__=="__main__":

    file_name = "established_news_2020-01-02.csv"
    data_path = os.path.join(".", "data", "buzzsumo_domain_name", file_name)
    df = pd.read_csv(data_path)

    df['date'] = [datetime.fromtimestamp(x).date() for x in df['published_date']]
    print(df.domain_name.unique())

    plot_platform_metrics(df)
    save_main_figure()

    for domain_name in df['domain_name'].unique():
        temp_df = df[df['domain_name']==domain_name]
        plot_platform_metrics(temp_df, domain_name)
        save_main_figure(domain_name.split('.')[0])


