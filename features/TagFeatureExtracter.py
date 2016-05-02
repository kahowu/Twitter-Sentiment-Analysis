
from FeatureExtracter import FeatureExtracter

class TagFeatureExtracter(FeatureExtracter):
    def __init__(self, tag_file):
        self.tag_set = set()
        f = open(tag_file)
        for line in f:
            self.tag_set.add(line.strip())
        f.close()

    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for token, tag in sent:
                if tag in self.tag_set:
                    # print tag
                    count += 1
        return count
