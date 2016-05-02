
from FeatureExtracter import FeatureExtracter

class FutureTenseExtracter(FeatureExtracter):
    def extract(self, tweet_sents):
        count = 0
        for sent in tweet_sents:
            if not sent:
                continue
            for i in range(len(sent)):
                token, tag = sent[i]
                if token == "'ll" or token == 'will' or token == 'gonna' or \
                        (i <= len(tweet_sents) - 2 and token == 'going' and sent[i + 1][0] == 'to' and  sent[i + 2][1] == 'VB'):
                    count += 1
        return count
