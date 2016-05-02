
from FeatureExtracter import FeatureExtracter


class SentCountExtracter(FeatureExtracter):
    def extract(self, tweet_sents):
        return len(tweet_sents)
