
all: OUT/mad/stats.md  OUT/mad/best_papers.md \
     OUT/mad/best_hashtags.md \
	 OUT/vis/act_spec_01.svg

OUT/mad/best_papers.md : ./print_best_papers.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis 
	./print_best_papers.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@ 

OUT/mad/stats.md : print_tweet_stats.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis 
	./print_tweet_stats.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_hashtags.md : print_best_hashtags.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis 
	./print_best_hashtags.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@

OUT/mad/best_users.md : print_best_users.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis 
	./print_best_users.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz > $@


OUT/vis/act_spec_01.svg : plot_activity_by_spec.py DATA/arxiv.json.gz DATA/twitter.json.gz common.py
	mkdir -p OUT/mad OUT/vis 
	./plot_activity_by_spec.py --arxiv-fname DATA/arxiv.json.gz --twitter-fname DATA/twitter.json.gz 


clean:
	rm -rf OUT
