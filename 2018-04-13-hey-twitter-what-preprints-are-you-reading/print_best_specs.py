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
    spec_to_counts = Counter()

    with gzip.open(args.arxiv_fname) as arxiv_f:
        id_to_metadata = json.loads(arxiv_f.read())

    with gzip.open(args.twitter_fname) as twitter_f:
        for line in twitter_f:
            tweet = json.loads(line)
            specs = set()
            for id in tweet['arxiv_ids']:
                metadata = id_to_metadata.get(id, {})
                if metadata:
                    specs.update(metadata['header']['setSpec'])
            specs = map(c.normalize_spec, specs)
            spec_to_counts.update(specs)

    print('| Ranking | Count | Spec |')
    print('|:---:|:---:|:---:|:---:|')

    for (i, (spec, count)) in enumerate(spec_to_counts.most_common(), 1):
        print('| %2d | %5d | %s |' % (i, count, spec))

if __name__ == '__main__':
    main(parse(sys.argv[1:]))
