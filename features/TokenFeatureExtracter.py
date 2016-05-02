
from FeatureExtracter import FeatureExtracter

class TokenFeatureExtracter(FeatureExtracter):
    def __init__(self, token_file):
        self.token_set = set()
        self.token_file = token_file
        f = open(token_file)
        for line in f:
            self.token_set.add(line.strip().lower())
        f.close()

    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for token, tag in sent:
                if token in self.token_set:
                    # print token, self.token_file
                    count += 1
        return count
