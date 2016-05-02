
from FeatureExtracter import FeatureExtracter
import re

class UpperCaseWordExtracter(FeatureExtracter):
    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for token, tag in sent:
                if len(token) >= 2 and token.isupper():
                    count += 1
        return count
