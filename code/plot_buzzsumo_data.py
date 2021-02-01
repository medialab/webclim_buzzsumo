import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


file_name = "established_news_cnn.csv"
data_path = os.path.join(".", "data", "buzzsumo_domain_name", file_name)
df = pd.read_csv(data_path)

print(df.columns)
df = df[df['domain_name']=='cnn.com']

df['date'] = [datetime.fromtimestamp(x).date() for x in df['published_date']]

plt.figure(figsize=(10, 5))

plt.title('CNN.com', fontsize='x-large')

plt.plot(df.groupby(by=["date"])["total_facebook_shares"].mean(), 
        label="Average Facebook shares")
plt.plot(df.groupby(by=["date"])["twitter_shares"].mean(), 
        label="Average Twitter shares")

plt.legend()
plt.tight_layout()
figure_path = os.path.join('.', 'figure', 'cnn.png')
plt.savefig(figure_path)
