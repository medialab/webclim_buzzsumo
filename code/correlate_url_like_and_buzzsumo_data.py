import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def import_input_csv(domain_name):
    file_name = domain_name.split('.')[0] + ".csv"
    data_path = os.path.join(".", "data", "facebook_url_like", file_name)
    df = pd.read_csv(data_path)
    return df


if __name__=="__main__":

    df_1 = import_input_csv('nytimes.com')
    df_2 = import_input_csv('nypost.com')
    df_3 = import_input_csv('breitbart.com')

    plt.figure(figsize=(6, 5))

    plt.plot(df_1['approx_likes_int'], df_1['total_facebook_shares'], '.', color='C0', label='nytimes.com', alpha=0.3)
    plt.plot(df_2['approx_likes_int'], df_2['total_facebook_shares'], '.', color='C1', label='nypost.com', alpha=0.3)
    plt.plot(df_3['approx_likes_int'], df_3['total_facebook_shares'], '.', color='C2', label='breitbart.com', alpha=0.3)

    plt.plot([0, 1000000], [0, 1000000], color='grey', linestyle='dotted', label='y = x')
    plt.legend()

    plt.ylabel('Total Facebook shares from Buzzsumo')
    plt.xlabel('Scraping the Plugin like button')
    plt.xlim([-1, 1000])
    plt.ylim([-1, 1000])

    plt.tight_layout()
    figure_name = 'correlation_bz_vs_scrap_1.png'
    figure_path = os.path.join('.', 'figure', figure_name)
    plt.savefig(figure_path)
    print("The '{}' figure is saved.".format(figure_name))