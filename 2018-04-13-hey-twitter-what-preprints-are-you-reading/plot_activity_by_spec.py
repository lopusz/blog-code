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


def normalize_spec(spec):
    return spec.split(':')[-1]


def main(args):
    id_to_metadata = c.read_id_to_metadata(args.arxiv_fname)

    tweets = c.read_tweets(args.twitter_fname)

    specs = [ 'cs', 'stat', 'math', 'astro-ph', 'physics',
              'cond-mat', 'hep-th', 'hep-ph', 'quant-ph', 'q-bio']

    for i, spec in enumerate(specs, 1):
        tweets_spec = c.filter_tweets_by_spec(tweets, spec, id_to_metadata)
        plot_fname = args.out_plots_fformat % i
        c.plot_hist(tweets_spec, plot_fname, False, title=spec)


if __name__ == '__main__':
    main(parse(sys.argv[1:]))