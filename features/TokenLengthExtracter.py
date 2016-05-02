
from FeatureExtracter import FeatureExtracter
import string

class TokenLengthExtracter(FeatureExtracter):
    def __init__(self):
        self.exclude = set(string.punctuation)
    def extract(self, tweet_sents):
        token_count = 0
        char_count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for token, tag in sent:
                skip = False
                for ch in token:
                    if ch in self.exclude:
                        skip = True
                        break
                if not skip:
                    token_count += 1
                    char_count += len(token)
        return float(char_count) / token_count if token_count else 0
