
all: OUT/mad/stats.md \
     OUT/mad/best_papers.md \
     OUT/mad/best_hashtags.md OUT/mad/best_specs.md OUT/mad/best_url_types.md \
	 OUT/mad/best_users.md \
	 OUT/mad/best_papers_best_tweets.md \
	 OUT/vis/act_spec_01.svg \


OUT/mad/stats.md : print_tweet_stats.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad
	./print_tweet_stats.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_papers.md : ./print_best_papers.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad
	./print_best_papers.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_specs.md : ./print_best_specs.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad
	./print_best_specs.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_users.md : print_best_users.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis
	./print_best_users.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_hashtags.md : print_best_hashtags.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad
	./print_best_hashtags.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_url_types.md : print_best_url_types.sh DATA/arxiv.json.gz DATA/twitter.json.gz
	mkdir -p OUT/mad
	./print_best_url_types.sh DATA/twitter.json.gz > $@

OUT/vis/act_spec_01.svg : plot_activity_by_spec.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/vis
	./plot_activity_by_spec.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz \
	                           --out-plots-fformat 'OUT/vis/act_spec_%02d.svg'

OUT/mad/best_papers_best_tweets.md : plot_activity_by_arxiv_id.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/vis
	mkdir -p OUT/mad
	./plot_activity_by_arxiv_id.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz \
	                               --out-plots-fformat 'OUT/vis/act_id_%02d.svg' \
	                               --out-stacked-plots-fformat 'OUT/vis/act_id_stacked_%02d.svg' \
								   > $@


clean:
	rm -rf OUT
