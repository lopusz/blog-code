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
        user_screen_name_counts = Counter()

        for tweet in tweets_spec:
            user_screen_name_counts[tweet['user_screen_name']] +=1


        s='* **%s** --- ' % spec
        spec_strings = []

        for (i, (spec, count)) in enumerate(user_screen_name_counts.most_common(5), 1):
            spec_strings += ['%s (%d)' % (spec, count)]
        s += ', '.join(spec_strings)
        print(s)


    # tweets_spec = c.filter_tweets_by_spec(tweets, 'math', id_to_metadata)
    # tweets_date = c.filter_tweets_by_time(tweets_spec,
    #                                       '2018-03-28 00:00:00',
    #                                       '2018-03-29 00:00:00')

    # for t in tweets_date:
    #     print(json.dumps(t))

if  __name__ == '__main__':
    main(parse(sys.argv[1:]))
