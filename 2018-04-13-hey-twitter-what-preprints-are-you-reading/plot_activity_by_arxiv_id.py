#!/usr/bin/env python

import argparse
import sys
import json

from collections import Counter
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
    parser.add_argument('--out-stacked-plots-fformat',
                        dest='out_stacked_plots_fformat',
                        action='store', required=True)
    return parser.parse_args(argv)


def make_id_str_to_tweet(tweets):
    for t in tweets:
        if t.get('id_str', None) is None:
            print(t)
    return { t['id_str'] : t for t in tweets}


def make_retweet_id_str_to_count(tweets):
    res = Counter()
    for t in tweets:
        res[t['retweet_id_str']] += 1
    return res


def make_id_count_lists(tweet_id_str_to_count, count_min):

    id_strs, counts = [], []

    for id_str, count in tweet_id_str_to_count.most_common():
        if count < count_min:
            break
        else:
            id_strs.append(id_str), counts.append(count)

    return id_strs, counts


def make_list_of_tweet_filters(retweet_id_strs):

    def _filter_tweets_without_retweet_id_strs(tweets):
        return [ t for t in tweets
                 if t['retweet_id_str'] not in retweet_id_strs ]
    res = []

    for retweet_id_str in retweet_id_strs:
        res.append(lambda tweets, i=retweet_id_str :
                    c.filter_tweets_by_retweet_id_str(tweets, i))

    res.append(_filter_tweets_without_retweet_id_strs)
    return res


def main(args):
    N=10

    tweets = c.read_tweets(args.twitter_fname)
    id_to_metadata = c.read_id_to_metadata(args.arxiv_fname)

    c.plot_hist(tweets, (args.out_plots_fformat % 0), False, title='All')

    id_to_count = c.get_arxiv_id_counter(tweets)

    for i, (arxiv_id, arxiv_id_tweet_count) \
                in enumerate(id_to_count.most_common(N), 1):
        tweets_id = c.filter_tweets_by_arxiv_id(tweets, arxiv_id)
        id_str_to_tweet = make_id_str_to_tweet(tweets_id)
        retweet_id_str_to_count = make_retweet_id_str_to_count(tweets_id)

        paper_title = id_to_metadata[arxiv_id]['metadata_arXiv']['title']
        paper_title = paper_title.replace('\n',' ')
        print('* [%s](http://arxiv.org/abs/%s) was tweeted %d times,'
              ' out of this\n'
               % (paper_title, arxiv_id, arxiv_id_tweet_count, ))

        id_strs, counts = make_id_count_lists(retweet_id_str_to_count, 20)
        for j, (id_str, count) in enumerate(zip(id_strs, counts), 1):
            tweet_text = id_str_to_tweet[id_str]['text'].replace('\n', ' ')
            print('    * %d, [Top tweet #%d](http://twitter.com/statuses/%s)' %
                    (count, j, id_str))
            print('      > %s\n' % tweet_text)
        plot_fname = args.out_plots_fformat % i
        c.plot_hist(tweets_id, plot_fname, False, title=arxiv_id)
        filter_fns = make_list_of_tweet_filters(id_strs)
        stacked_plot_fname = args.out_stacked_plots_fformat % i
        c.plot_stacked_hist(tweets_id, stacked_plot_fname,
                            logscale=False,
                            title=paper_title,
                            filter_tweets_fns=filter_fns)

if __name__ == '__main__':
    main(parse(sys.argv[1:]))