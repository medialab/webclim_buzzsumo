import os

import pandas as pd
pd.set_option('display.max_rows', None)


if __name__=="__main__":

    df_path = os.path.join('.', 'data', 'sciencefeedback', 'appearances_2021-01-04_.csv')
    df = pd.read_csv(df_path)

    vc = df.domain_name.value_counts()

    misinfo_list = vc[vc >= 8].index.to_list()
    print(len(misinfo_list))

    platforms = [
        'youtube.com',
        'facebook.com',
        'bitchute.com',
        'twitter.com',
        'wordpress.com',
        'lbry.tv',
        'instagram.com',
        'archive.org',
        'banned.video',
        'vimeo.com',
        'iheart.com',
        'brandnewtube.com',
    ]
    print(len(platforms))

    duplicate = 'principia-scientific.org'

    misinfo_list = [x for x in misinfo_list if x not in platforms]
    misinfo_list.remove(duplicate)
    for x in misinfo_list:
        print(x)
    print(len(misinfo_list))
