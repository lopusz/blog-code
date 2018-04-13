
import datetime as dt
import gzip
import json

import numpy as np

import matplotlib as mplt

mplt.use('Agg')
import matplotlib.pyplot as plt

def normalize_spec(spec):
    return spec.split(':')[-1]

def _contains_spec(spec, tweet, id_to_metadata):
    specs = set()
    for id in tweet['arxiv_ids']:
        metadata = id_to_metadata.get(id, {})
        if metadata:
            specs.update(metadata['header']['setSpec'])
    specs = map(normalize_spec, specs)
    return spec in specs


def plot_hist(tweets, plot_fname, logscale, title):
    HIS_WIDTH = 2 * 3600.0

    ts = [ t['timestamp_ms']/1000.0 for t in tweets ]
    bins_ts_min = dt.datetime(year=2018, month=3, day=21).timestamp()
    bins_ts_max = dt.datetime(year=2018, month=4, day=13).timestamp() + \
                  0.5 * HIS_WIDTH
    bins = np.arange(bins_ts_min, bins_ts_max, HIS_WIDTH)
    hist, bins = np.histogram(ts, bins=bins)
    bins_center = (bins[:-1] + bins[1:]) / 2

    # Preparing xtics
    midnights = [dt.datetime(hour=0, minute=0, second=0, day=22, month=3,
                             year=2018)]
    while midnights[-1] < dt.datetime.fromtimestamp(bins[-1]):
        midnights.append(midnights[-1] + dt.timedelta(seconds=24 * 3600.0))
    midnights = midnights[:-1]
    midnights_ts = [m.timestamp() for m in midnights]
    midnights_labels = [m.strftime('%m-%d ') for m in midnights]
    for i in range(1, len(midnights_labels), 2):
        midnights_labels[i] = ''
    # Preparing weekend lines
    weekends_dt = [dt.datetime(year=2018, month=3, day=24, hour=0, minute=0),
                   dt.datetime(year=2018, month=3, day=26, hour=0, minute=0),
                   dt.datetime(year=2018, month=3, day=31, hour=0, minute=0),
                   dt.datetime(year=2018, month=4, day=2, hour=0, minute=0),
                   dt.datetime(year=2018, month=4, day=7, hour=0, minute=0),
                   dt.datetime(year=2018, month=4, day=9, hour=0, minute=0) ]

    fig = plt.figure(figsize=(8, 4  ))
    fig.suptitle(title)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([bins[0], bins[-1]])
    if logscale:
        ax.set_yscale('log')
        ax.set_ylim([1.0e0, 1.0e4])

    plt.bar(bins_center, hist, align='center', width=HIS_WIDTH)
    plt.xlabel('time')
    plt.ylabel('tweet counts')

    ax.set_axisbelow(True)
    for i in range(0,len(weekends_dt)-1,2):
        plt.axvspan(weekends_dt[i].timestamp(),
                    weekends_dt[i+1].timestamp(),
                    color='lightgray', zorder=-1)
    plt.grid()
    plt.xticks(midnights_ts, midnights_labels)
    fig.savefig(plot_fname, dpi=240, bbox_inches='tight')
    plt.close(fig)


def read_tweets(fname):
    tweets = []
    with gzip.open(fname) as twitter_f:
        for line in twitter_f:
            tweets.append(json.loads(line))
    return tweets

def filter_tweets_by_spec(tweets, spec, id_to_metadata):
    return [t for t in tweets if _contains_spec(spec, t, id_to_metadata)]

def filter_tweets_by_id(tweets, id):
    return [t for t in tweets if id in t['arxiv_ids']]

def filter_tweets_by_time(tweets, min_yyyy_mm_dd_hhmmss, max_yyyy_mm_dd_hhmmss):
    ts_min = 1000.0*dt.datetime.\
        strptime(min_yyyy_mm_dd_hhmmss, '%Y-%m-%d %H:%M:%S').timestamp()
    ts_max = 1000.0*dt.datetime.\
        strptime(max_yyyy_mm_dd_hhmmss, '%Y-%m-%d %H:%M:%S').timestamp()

    return [t for t in tweets
            if t['timestamp_ms'] < ts_max and t['timestamp_ms'] >= ts_min]

def read_id_to_metadata(fname):
    with gzip.open(fname) as arxiv_f:
        id_to_metadata = json.loads(arxiv_f.read())
    return id_to_metadata
