#!/usr/bin/env python

import argparse
import datetime as dt
import gzip
import json
import sys

import common as c

def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--arxiv-fname', dest='arxiv_fname',
                        action='store', required=True)
    parser.add_argument('--twitter-fname',
                        dest='twitter_fname',
                        action='store', required=True)
    parser.add_argument('--out-plots-fformat',
                        dest='out_plots_fformat',
                        action='store', required=True)
    return parser.parse_args(argv)


def main(args):
    N=10

    tweets = c.read_tweets(args.twitter_fname)
    c.plot_hist(tweets, (args.out_plots_fformat % 0), False, title='All')

    id_to_count = c.get_arxiv_id_counter(tweets)

    for i, (id, _) in enumerate(id_to_count.most_common(N), 1):
        tweets_id = c.filter_tweets_by_arxiv_id(tweets, id)
        plot_fname = args.out_plots_fformat % i
        c.plot_hist(tweets_id, plot_fname, False, title=id)


if __name__ == '__main__':
    main(parse(sys.argv[1:]))