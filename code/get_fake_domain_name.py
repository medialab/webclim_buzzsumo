import os

import pandas as pd


if __name__=="__main__":

    df_path = os.path.join('.', 'data', 'sciencefeedback', 'appearances_2021-01-04_.csv')
    df = pd.read_csv(df_path)

    vc = df.domain_name.value_counts()
    print(vc[vc >= 20])
