import os

import pandas as pd
pd.set_option('display.max_rows', None)


if __name__=="__main__":

    df_path = os.path.join('.', 'data', 'sciencefeedback', 'appearances_2021-01-04_.csv')
    df = pd.read_csv(df_path)

    vc = df.domain_name.value_counts()

    # misinfo_list = vc[vc >= 8].index.to_list()
    misinfo_list = vc[(vc < 8) & (vc >= 4)].index.to_list()
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
        'parler.com',
        'dailymotion.com',
        'rumble.com',
        'home.blog',
        '2020electioncenter.com',
        'scribd.com',
        'brighteon.com',
        'newtube.app'
    ]

    misinfo_list = [x for x in misinfo_list if x not in platforms]
    if 'principia-scientific.org' in misinfo_list:
        misinfo_list.remove('principia-scientific.org')
    for x in misinfo_list:
        print("'", x, "',", sep = '')
    print(len(misinfo_list))
