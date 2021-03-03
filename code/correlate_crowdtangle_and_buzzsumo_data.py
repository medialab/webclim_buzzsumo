import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__=="__main__":

    domain_name_1 = 'nytimes.com'
    file_name = domain_name_1.split('.')[0] + ".csv"
    data_path = os.path.join(".", "data", "crowdtangle_url", file_name)
    df_1 = pd.read_csv(data_path)
    df_1['date'] = [datetime.fromtimestamp(x).date() for x in df_1['published_date']]
    print(np.min(df_1['date']), np.max(df_1['date']))

    domain_name_2 = 'breitbart.com'
    file_name = domain_name_2.split('.')[0] + ".csv"
    data_path = os.path.join(".", "data", "crowdtangle_url", file_name)
    df_2 = pd.read_csv(data_path)
    df_2['date'] = [datetime.fromtimestamp(x).date() for x in df_2['published_date']]
    print(np.min(df_2['date']), np.max(df_2['date']))

    columns_bz = [
        'facebook_likes',
        'facebook_comments',
        'facebook_shares',
    ]

    columns_ct = [
        'like_count',
        'share_count',
        'comment_count',
    ]

    plt.figure(figsize=(6, 15))

    for i in range(len(columns_bz)):

        plt.subplot(len(columns_bz), 1, i + 1)

        plt.plot(df_1[columns_ct[i]], df_1[columns_bz[i]], '.', color='C0', label='nytimes.com')
        plt.plot(df_2[columns_ct[i]], df_2[columns_bz[i]], '.', color='C1', label='breitbart.com')
        plt.plot([0, 1000000], [0, 1000000], color='grey', linestyle='dotted', label='y = x')
        plt.legend()

        plt.yscale('log')
        plt.xscale('log')
        plt.ylabel('Buzzsumo')
        plt.xlabel('CrowdTangle')
        plt.title(columns_bz[i])

    plt.tight_layout()
    figure_name = 'correlation_bz_vs_ct.png'
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))