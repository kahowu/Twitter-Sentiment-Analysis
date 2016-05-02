
from abc import ABCMeta, abstractmethod

class FeatureExtracter:
    __metaclass__ = ABCMeta
    @abstractmethod
    def extract(self, tweet):
        pass