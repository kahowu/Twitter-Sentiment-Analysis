
from FeatureExtracter import FeatureExtracter
import re

class SentLengthExtracter(FeatureExtracter):
    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            count += len(sent)
        return float(count) / len(tweet_sents) if len(tweet_sents) else 0
