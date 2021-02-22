import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__=="__main__":

    domain_name = 'cnn.com'
    # domain_name = 'nyposts.com'

    file_name = "%s_posts.csv" % domain_name.split('.')[0]
    data_path = os.path.join(".", "data", "crowdtangle_domain_name", file_name)
    ct_df = pd.read_csv(data_path, dtype=str)

    ct_df['date'] = pd.to_datetime(ct_df['date'])
    ct_df["facebook_shares"]   = ct_df[["actual_share_count"]].astype(int)
    ct_df["facebook_comments"] = ct_df[["actual_comment_count"]].astype(int)
    ct_df["facebook_likes"] = ct_df[["actual_like_count"]].astype(int)

    file_name = "established_news_2020-01-02.csv"
    data_path = os.path.join(".", "data", "buzzsumo_domain_name", file_name)
    bz_df = pd.read_csv(data_path)

    bz_df = bz_df[bz_df['domain_name']==domain_name]
    bz_df['date'] = [datetime.fromtimestamp(x).date() for x in bz_df['published_date']]

    columns_to_plot = [
        'facebook_likes',
        'facebook_comments',
        'facebook_shares',
    ]

    plt.figure(figsize=(10, 12))

    for subplot_index in range(len(columns_to_plot)):

        ax = plt.subplot(len(columns_to_plot), 1, subplot_index + 1)

        plt.plot(bz_df.groupby(by=["date"])[columns_to_plot[subplot_index]].sum(),
                label='Buzzsumo', color='C0')
        plt.plot(ct_df.groupby(by=["date"])[columns_to_plot[subplot_index]].sum(),
                label='Crowdtangle', color='C1')
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
        plt.ylabel(columns_to_plot[subplot_index])

        if subplot_index == 0:
            plt.title(domain_name, fontsize='x-large')

    plt.tight_layout()

    figure_name = 'comparison_' + domain_name.split('.')[0] + '.png'
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))