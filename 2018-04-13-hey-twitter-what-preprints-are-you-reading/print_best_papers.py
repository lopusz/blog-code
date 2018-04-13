#!/usr/bin/env python

import argparse
import json
import gzip
import sys

from collections import Counter


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--arxiv-fname', dest='arxiv_fname',
                        action='store', required=True)
    parser.add_argument('--twitter-fname',
                        dest='twitter_fname',
                        action='store', required=True)
    return parser.parse_args(argv)


def normalize_spec(spec):
    return spec.split(':')[-1]


def main(args):
    id_to_counts = Counter()
    with gzip.open(args.twitter_fname) as twitter_f:
        for line in twitter_f:
            tweet = json.loads(line)
            for id in tweet['arxiv_ids']:
                id_to_counts[id] += 1

    with gzip.open(args.arxiv_fname) as arxiv_f:
        id_to_metadata = json.loads(arxiv_f.read())
    print('| Ranking | Tweets | Spec | Title | Pdf|')
    print('|:---:|:---:|:---:|-------|---:|')

    for (lp, (id, count)) in enumerate(id_to_counts.most_common(10),1):
        abs_url = 'http://arxiv.org/abs/%s' % id
        pdf_url = 'http://arxiv.org/pdf/%s' % id
        metadata = id_to_metadata.get(id, {})
        if metadata:
            title = metadata['metadata_arXivRaw']['title']
            title = title.replace('\n','')
            specs  = [normalize_spec(s) for s in metadata['header']['setSpec']]
            specs_str = '/'.join(specs)

            print('%2d | %4d | %10s | [%s](%s) | [here](%s) |' %
                  (lp, count, specs_str, title, abs_url, pdf_url))
        else:
            print('%2d | %4d | %10s | [%s](%s) | [here](%s) |' %
                  (lp, count, '?', '?', abs_url, abs_url, pdf_url))


if __name__ == '__main__':
    main(parse(sys.argv[1:]))
