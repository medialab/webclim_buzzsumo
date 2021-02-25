import pandas as pd 
import numpy as np


df = pd.read_csv('./test.csv')
print(np.sum(df['actual_like_count'].values))