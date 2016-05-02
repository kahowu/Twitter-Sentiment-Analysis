
from FeatureExtracter import FeatureExtracter
import re

class EllipsisExtracter(FeatureExtracter):
    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for token, tag in sent:
                if re.match(r'\.\.\.+', token):
                    count += 1
        return count
