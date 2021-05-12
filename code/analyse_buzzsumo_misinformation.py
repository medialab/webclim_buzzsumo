from datetime import datetime, timedelta
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats

from utils import import_data, save_figure


pd.options.display.max_rows = None


def import_buzzsumo_data():

    df_bz_1 = import_data('buzzsumo_domain_name', 'misinformation_2021-03-23.csv')
    df_bz_2 = import_data('buzzsumo_domain_name', 'misinformation_2021-03-30.csv')
    df_bz = pd.concat([df_bz_1, df_bz_2])

    df_bz['date'] = [datetime.fromtimestamp(x).date() for x in df_bz['published_date']]
    df_bz['date'] = pd.to_datetime(df_bz['date'])
    df_bz = df_bz.drop_duplicates(subset=['url'])

    return df_bz


def arrange_plot(ax):

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis="y")
    plt.locator_params(axis='y', nbins=4)

    plt.xlim(
        np.datetime64(datetime.strptime('2018-12-31', '%Y-%m-%d') - timedelta(days=4)), 
        np.datetime64(datetime.strptime('2021-01-01', '%Y-%m-%d') + timedelta(days=4))
    )


def get_strike_dates(df_url, domain_name):

    df_url_domain = df_url[df_url['domain_name']==domain_name]
    strike_dates = df_url_domain['Date of publication'].to_list()
    strike_dates = [np.datetime64(date) for date in strike_dates]
    strike_dates.sort()

    return strike_dates


def compute_repeat_offender_periods(strike_dates):

    repeat_offender_periods = []

    if len(strike_dates) > 1:
        for index in range(1, len(strike_dates)):
            if strike_dates[index] - strike_dates[index - 1] < np.timedelta64(90, 'D'):

                repeat_offender_periods.append([
                    strike_dates[index],
                    strike_dates[index - 1] + np.timedelta64(90, 'D')
                ])

    return repeat_offender_periods


def merge_overlapping_periods(overlapping_periods):
    
    if len(overlapping_periods) == 0:
        return []
    
    else:
        overlapping_periods.sort(key=lambda interval: interval[0])
        merged_periods = [overlapping_periods[0]]

        for current in overlapping_periods:
            previous = merged_periods[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged_periods.append(current)

        return merged_periods


def rolling_average(df, column):
    return df.resample('D', on='date')[column].mean().rolling(window=7, win_type='triang', center=True).mean()


def plot_one_domain(df_bz, domain_name, strike_dates, ax):

    df_bz_domain = df_bz[df_bz['domain_name']==domain_name]

    plt.plot(rolling_average(df_bz_domain, 'facebook_likes'), 
        label="Reactions per article", color="C0")
    plt.plot(rolling_average(df_bz_domain, 'facebook_shares'), 
        label="Shares per article", color="C1")
    plt.plot(rolling_average(df_bz_domain, 'facebook_comments'), 
        label="Comments per article", color="C2")

    scale_y = np.nanmax([rolling_average(df_bz_domain, 'facebook_likes'),
                        rolling_average(df_bz_domain, 'facebook_shares'),
                        rolling_average(df_bz_domain, 'facebook_comments')])/10

    for date in strike_dates:
        plt.arrow(x=date, y=0, dx=0, dy=-scale_y, color='C3')

    repeat_offender_periods = compute_repeat_offender_periods(strike_dates)
    repeat_offender_periods = merge_overlapping_periods(repeat_offender_periods)
    for period in repeat_offender_periods:
        plt.axvspan(period[0], period[1], ymin=1/11, facecolor='C3', alpha=0.1)

    ax.spines['bottom'].set_visible(False)
    plt.hlines(0, xmin=np.datetime64('2018-12-17'), xmax=np.datetime64('2021-01-04'), linewidths=1, color='k')
    ax.spines['bottom'].set_visible(False)
    plt.ylim(bottom=-scale_y)

    arrange_plot(ax)


def plot_example_domain(df_bz, df_url, ax):

    domain_name = 'americanthinker.com'

    strike_dates = get_strike_dates(df_url, domain_name)
    plot_one_domain(df_bz, domain_name, strike_dates, ax)

    legend1 = plt.legend(loc='upper left')
    patch1 = mpatches.Patch(facecolor='white', alpha=0.4, edgecolor='k')
    patch2 = mpatches.Patch(facecolor='pink', alpha=0.4, edgecolor='k')
    legend2 = plt.legend([patch1, patch2], ["'No strike' periods", "'Repeat offender' periods"],
                loc='upper right', framealpha=1)
    plt.gca().add_artist(legend1)

    plt.title("Engagement metrics for one example 'repeat offender' domain name (" + domain_name + ")")
    
    plt.text(
        s='Known strikes', color='C3', fontweight='bold',
        x=np.datetime64('2019-12-20'), horizontalalignment='right', 
        y=-500, verticalalignment='top'
    )


def keep_repeat_offender_posts(df_bz, domain_name, repeat_offender_periods):
    
    if len(repeat_offender_periods) == 0:
        return pd.DataFrame()
    
    df_bz_domain = df_bz[df_bz['domain_name']==domain_name]

    repeat_offender_df_list = []
    for repeat_offender_period in repeat_offender_periods:
        new_df = df_bz_domain[(df_bz_domain['date'] >= repeat_offender_period[0]) &
                              (df_bz_domain['date'] <= repeat_offender_period[1])]
        if len(new_df) > 0:
            repeat_offender_df_list.append(new_df)
    
    if len(repeat_offender_df_list) > 0:
        return pd.concat(repeat_offender_df_list)
    else:
        return pd.DataFrame()


def keep_free_posts(df_bz, domain_name, repeat_offender_periods):
    
    df_bz_domain = df_bz[df_bz['domain_name']==domain_name]
    if len(repeat_offender_periods) == 0:
        return df_bz_domain
    
    free_df_list = []
    for ro_index in range(len(repeat_offender_periods) + 1):
        if ro_index == 0:
            new_df = df_bz_domain[df_bz_domain['date'] < repeat_offender_periods[0][0]]
        elif ro_index == len(repeat_offender_periods):
            new_df = df_bz_domain[df_bz_domain['date'] > repeat_offender_periods[-1][1]]
        else:
            new_df = df_bz_domain[(df_bz_domain['date'] > repeat_offender_periods[ro_index - 1][1]) &
                                  (df_bz_domain['date'] < repeat_offender_periods[ro_index][0])]
        if len(new_df) > 0:
            free_df_list.append(new_df)
    
    if len(free_df_list) > 0:
        return pd.concat(free_df_list)
    else:
        return pd.DataFrame()


def compute_periods_average(df_bz, df_url):

    repeat_offender = {
        'reaction': [],
        'share': [],
        'comment': []
    }
    free = {
        'reaction': [],
        'share': [],
        'comment': []
    }

    for domain_name in df_bz['domain_name'].unique():
            
        strike_dates = get_strike_dates(df_url, domain_name)
        repeat_offender_periods = compute_repeat_offender_periods(strike_dates)
        repeat_offender_periods = merge_overlapping_periods(repeat_offender_periods)
        
        repeat_offender_df = keep_repeat_offender_posts(df_bz, domain_name, repeat_offender_periods)
        free_df            = keep_free_posts(df_bz, domain_name, repeat_offender_periods)
        
        if (len(repeat_offender_df) > 100) & (len(free_df) > 100):
            
            repeat_offender['reaction'].append(np.mean(repeat_offender_df['facebook_likes']))
            free['reaction'].append(np.mean(free_df['facebook_likes']))
            
            repeat_offender['share'].append(np.mean(repeat_offender_df['facebook_shares']))
            free['share'].append(np.mean(free_df['facebook_shares']))
            
            repeat_offender['comment'].append(np.mean(repeat_offender_df['facebook_comments']))
            free['comment'].append(np.mean(free_df['facebook_comments']))

    return repeat_offender, free


def print_repeat_offender_statistics(repeat_offender, free):

    w, p = stats.wilcoxon(repeat_offender['reaction'], free['reaction'])
    print('Wilcoxon test between the reactions: w =', w, ', p =', p)
    
    w, p = stats.wilcoxon(repeat_offender['share'], free['share'])
    print('Wilcoxon test between the shares: w =', w, ', p =', p)

    w, p = stats.wilcoxon(repeat_offender['comment'], free['comment'])
    print('Wilcoxon test between the comments: w =', w, ', p =', p, '\n')


def calculate_confidence_interval(sample):

    averages = []
    for bootstrap_index in range(1000):
        resampled_sample = random.choices(sample, k=len(sample))
        averages.append(np.mean(resampled_sample))

    return np.percentile(averages, 5), np.percentile(averages, 95)


def plot_repeat_offender_average(repeat_offender, free, ax):

    width = .25
    labels = ['Reactions', 'Shares', 'Comments']
    x = np.arange(len(labels)) 

    # Plot the bars
    plt.bar(x - width/2, [np.mean(free['reaction']), np.mean(free['share']), np.mean(free['comment'])], 
                    width, label="'No strike' periods", color='white', edgecolor=[.2, .2, .2], zorder=3)

    plt.bar(x + width/2, [np.mean(repeat_offender['reaction']), np.mean(repeat_offender['share']), 
                                        np.mean(repeat_offender['comment'])], 
                    width, label="'Repeat offender' periods", color='pink', edgecolor=[.2, .2, .2], zorder=3)

    # Add the error bars
    idx = 0   
    for metric in ['reaction', 'share', 'comment']:
        low, high = calculate_confidence_interval(free[metric])
        plt.errorbar(idx - width/2, np.mean(free[metric]), 
            yerr=[[np.mean(free[metric]) - low], [high - np.mean(free[metric])]], 
            color=[.2, .2, .2], zorder=4, linestyle='')

        low, high = calculate_confidence_interval(repeat_offender[metric])
        plt.errorbar(idx + width/2, np.mean(repeat_offender[metric]), 
            yerr=[[np.mean(repeat_offender[metric]) - low], [high - np.mean(repeat_offender[metric])]], 
            color=[.2, .2, .2], zorder=4, linestyle='')

        idx += 1

    plt.legend(framealpha=1)

    plt.title("Engagement metrics averaged over {} 'repeat offender' domain names"\
        .format(len(repeat_offender['reaction'])))
    plt.xticks(x, labels, fontsize='large',)
    ax.tick_params(axis='x', which='both', length=0)
    plt.xlim([-.5, 2.5])
    ax.grid(axis="y", zorder=0)
    plt.locator_params(axis='y', nbins=4)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)


def plot_histogram(repeat_offender, free, title_detail):

    infowars = {
        'reaction': -94,
        'share': -96,
        'comment': -93
    }

    fig = plt.figure(figsize=(14, 12))
    fig.suptitle('Histogram of the percentage changes ' + title_detail + ' for the {} domain names'\
                .format(len(repeat_offender['reaction'])), fontsize='x-large')

    xlabels = [
        '-100%', '', '', '', '',
        '-50%', '', '', '', '',
        '0%', '', '', '', '',
        '+50%', '', '', '', '',
        '+100%', '', '', '', '',
        '+150%', 'More'
    ]

    columns_to_plot = ['reaction', 'share', 'comment']

    for index, column in enumerate(columns_to_plot):
        ax = plt.subplot(3, 1, index + 1)
        
        evolution_percentage = [(ro - fr) * 100 / fr for ro, fr in zip(repeat_offender[column], free[column])]
        evolution_percentage = [x for x in evolution_percentage if x != np.inf]
        plt.hist(evolution_percentage, bins=list(range(-100, 151, 10)) + [100000], color='C' + str(index))
        
        plt.vlines(0, 0, 10, color='k', linestyles='dotted')
        plt.vlines(infowars[column], 0, 3, color='C3', linestyles='dotted')
        plt.text(infowars[column] - 2, 3.2, 'Infowars drop', color='C3', rotation=50)
        
        plt.xlabel(column.capitalize() + 's')
        plt.xlim([-100, 160])
        plt.xticks(list(range(-100, 151, 10)) + [160], xlabels)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.locator_params(axis='y', nbins=4)

    plt.tight_layout()
    save_figure('histogram ' + title_detail + '.png')


def plot_figure_1(df_bz, df_url):

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 5)

    ax = fig.add_subplot(gs[0, :])
    plot_example_domain(df_bz, df_url, ax)

    ax = fig.add_subplot(gs[1, 1:4])
    repeat_offender, free = compute_periods_average(df_bz, df_url)
    print_repeat_offender_statistics(repeat_offender, free)
    plot_repeat_offender_average(repeat_offender, free, ax)
    plot_histogram(repeat_offender, free, "between the 'repeat offender' and the 'free' periods")

    plt.tight_layout()
    save_figure(figure_name='figure_1.png')


def plot_figure_2(df):
    
    plt.figure(figsize=(10, 12))

    ax = plt.subplot(311)
    plt.title("Average for the {} 'repeat offender' domain names".format(df.domain_name.nunique()), fontsize='x-large')

    arrange_plot(ax)
    plt.plot(df.groupby(by=["date"])["facebook_likes"].sum()/df.groupby(by=["date"])["domain_name"].nunique(), 
            label="Reactions per day", color="C0")
    plt.plot(df.groupby(by=["date"])["facebook_shares"].sum()/df.groupby(by=["date"])["domain_name"].nunique(), 
            label="Shares per day", color="C1")
    plt.plot(df.groupby(by=["date"])["facebook_comments"].sum()/df.groupby(by=["date"])["domain_name"].nunique(), 
            label="Comments per day", color="C2")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.ylim(0, 130000)
    plt.legend()

    ax = plt.subplot(312)
    arrange_plot(ax)
    plt.plot(df["date"].value_counts().sort_index()/df.groupby(by=["date"])["domain_name"].nunique(), 
        label="Articles per day", color=[.2, .2, .2])
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.legend()

    ax = plt.subplot(313)
    arrange_plot(ax)
    plt.plot(df.groupby(by=["date"])["facebook_likes"].sum()/df["date"].value_counts().sort_index(), 
            label="Reactions per article")
    plt.plot(df.groupby(by=["date"])["facebook_shares"].sum()/df["date"].value_counts().sort_index(), 
            label="Shares per article")
    plt.plot(df.groupby(by=["date"])["facebook_comments"].sum()/df["date"].value_counts().sort_index(), 
            label="Comments per article")
    plt.axvline(x=np.datetime64("2020-06-09"), color='black', linestyle='--', linewidth=1)
    plt.ylim(0, 6500)
    plt.legend()

    plt.tight_layout()
    save_figure(figure_name='figure_2.png')


def plot_figure_3(df_bz, df_url):

    domains_to_plot = [
        'breitbart.com',
        'sott.net',
        'thelibertybeacon.com',
        'theepochtimes.com',
        'newspunch.com',
        'therightscoop.com',
        'stillnessinthestorm.com',
        'thegatewaypundit.com',
        'theblaze.com',
        'wnd.com',
    ]

    fig = plt.figure(figsize=(10, 12))

    for idx in range(len(domains_to_plot)):

        ax = plt.subplot(5, 2, idx + 1)

        strike_dates = get_strike_dates(df_url, domains_to_plot[idx])
        plot_one_domain(df_bz, domains_to_plot[idx], strike_dates, ax)

        if idx == 0:
            plt.legend(loc='upper left')
        elif idx == 1:
            patch1 = mpatches.Patch(facecolor='white', alpha=0.4, edgecolor='k')
            patch2 = mpatches.Patch(facecolor='pink', alpha=0.4, edgecolor='k')
            plt.legend([patch1, patch2], ["'No strike' periods", "'Repeat offender' periods"],
                        loc='upper right', framealpha=1)

        arrange_plot(ax)
        plt.title(domains_to_plot[idx])

        xticks = [np.datetime64('2019-01-01'), np.datetime64('2019-05-01'), np.datetime64('2019-09-01'),
                np.datetime64('2020-01-01'), np.datetime64('2020-05-01'), np.datetime64('2020-09-01')
                ]
        plt.xticks(xticks, rotation=30, ha='right')

    plt.tight_layout()
    save_figure('figure_3.png')


if __name__=="__main__":

    # ['date', 'url', 'published_date', 'domain_name', 'total_shares',
    #    'alexa_rank', 'pinterest_shares', 'total_reddit_engagements',
    #    'twitter_shares', 'total_facebook_shares', 'facebook_likes',
    #    'facebook_comments', 'facebook_shares']
    df_bz = import_buzzsumo_data()
    df_url = import_data('sciencefeedback', 'appearances_2021-01-04_.csv')
    df_url = df_url.drop_duplicates(subset=['domain_name', 'Item reviewed'])

    plot_figure_1(df_bz, df_url)
    plot_figure_2(df_bz)
    plot_figure_3(df_bz, df_url)
