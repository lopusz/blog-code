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
    return parser.parse_args(argv)


def main(args):

    tweets = c.read_tweets(args.twitter_fname)
    c.plot_hist(tweets, 'OUT/vis/out0.svg', False, title='All')

    ids = [ '1803.02329', '1803.10122',
            '1804.01622', '1804.02717',
            '1804.02001', '1803.11203',
            '1803.08494', '1803.06959',
            '1804.02958', '1803.04994']
    # 1802.04291
    # 1707.09457
    # 1803.10882
    # 1803.08823
    # 1803.09820
    # 1803.03835
    # 1803.10237
    # 1704.04299
    for i, id in enumerate(ids, 1):
        tweets_id = c.filter_tweets_by_id(tweets, id)
        c.plot_hist(tweets_id, 'OUT/vis/act_id_%02d.svg' % i, False, title=id)



if __name__ == '__main__':
    main(parse(sys.argv[1:]))