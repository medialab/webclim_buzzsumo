import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz


input_path = os.path.join('.', 'data', 'buzzsumo_domain_name', 'infowars.csv')
df = pd.read_csv(input_path)
df['date'] = [datetime.fromtimestamp(x).date() for x in df['published_date']]

columns_to_plot = [
    "total_facebook_shares",
    "twitter_shares"
]

plt.figure(figsize=(10, 7))

for subplot_index in range(2):

    ax = plt.subplot(2, 1, subplot_index + 1)

    plt.plot(df.groupby(by=["date"])[columns_to_plot[subplot_index]].mean(),
            label=columns_to_plot[subplot_index], color='C' + str(subplot_index))
    plt.legend()

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

    if subplot_index == 0:
        plt.axvline(x=np.datetime64("2018-08-01"), color='black', linestyle='--', linewidth=1)
        plt.axvline(x=np.datetime64("2019-02-05"), color='black', linestyle='--', linewidth=1)
        plt.axvline(x=np.datetime64("2019-05-02"), color='black', linestyle='--', linewidth=1)
    elif subplot_index == 1:
        plt.axvline(x=np.datetime64("2019-05-02"), color='black', linestyle='--', linewidth=1)

    if subplot_index == 0:
        plt.title('infowars.com', fontsize='x-large')
        plt.ylim(top=5000)
    elif subplot_index == 1:
        plt.ylim(top=1000)

plt.tight_layout()

figure_path = os.path.join('.', 'figure', 'infowars_buzzsumo.png')
plt.savefig(figure_path)
print("The '{}' figure is saved.".format(figure_path))