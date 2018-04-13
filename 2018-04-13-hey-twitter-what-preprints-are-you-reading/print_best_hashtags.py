#!/usr/bin/env python

import argparse
import json
import gzip
import sys

from collections import Counter

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
    id_to_metadata = c.read_id_to_metadata(args.arxiv_fname)

    specs = [ 'cs', 'stat', 'math', 'astro-ph', 'physics',
              'cond-mat', 'hep-th', 'hep-ph', 'quant-ph', 'q-bio']

    for spec in specs:
        tweets_spec = c.filter_tweets_by_spec(tweets, spec, id_to_metadata)
        hashtag_to_counts = Counter()

        for tweet in tweets_spec:
            hashtags = tweet['hashtags']
            hashtag_to_counts.update(hashtags)

        s='* **%s** --- ' % spec
        spec_strings = []

        for (i, (spec, count)) in enumerate(hashtag_to_counts.most_common(5), 1):
            spec_strings += ['%s (%d)' % (spec, count)]
        s += ', '.join(spec_strings)
        print(s)

if __name__ == '__main__':
    main(parse(sys.argv[1:]))
