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


def conv_ts_to_str(ts):
    return dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')


def normalize_spec(spec):
    return spec.split(':')[-1]


def main(args):
    with gzip.open(args.arxiv_fname) as arxiv_f:
        id_to_metadata = json.loads(arxiv_f.read())

    tweets = []

    with gzip.open(args.twitter_fname) as twitter_f:
        for line in twitter_f:
            tweets.append(json.loads(line))

    specs = [ 'cs', 'stat', 'math', 'astro-ph', 'physics',
              'cond-mat', 'hep-th', 'hep-ph', 'quant-ph', 'q-bio']

    for i, spec in enumerate(specs, 1):
        tweets_spec = c.filter_tweets_by_spec(tweets, spec, id_to_metadata)
        c.plot_hist(tweets_spec,
                    'OUT/vis/act_spec_%02d.svg' % i, False, title=spec)



if __name__ == '__main__':
    main(parse(sys.argv[1:]))