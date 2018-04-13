#!/usr/bin/env python

import argparse
import datetime as dt
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

def conv_ts_to_str(ts):
    return dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')


def main(args):
    tweets = c.read_tweets(args.twitter_fname)
    ts = [ t['timestamp_ms']/1000.0 for t in tweets ]
    ts_min = min(ts)
    ts_max = max(ts)

    print(conv_ts_to_str(ts_min))
    print(conv_ts_to_str(ts_max))
    delta = dt.datetime.fromtimestamp(ts_max)-dt.datetime.fromtimestamp(ts_min)
    print(delta.total_seconds()/3600.0/24.)

    print(len(tweets))

    id_to_metadata = c.read_id_to_metadata(args.arxiv_fname)
    print(len(id_to_metadata))

if __name__ == '__main__':
    main(parse(sys.argv[1:]))