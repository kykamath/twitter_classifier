'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import DataType, Settings
import pprint
class DocumentFormatUnigram(object):
    def __init__(self, currentTime):
        self.currentTime = currentTime
        self.combinedSetFile = Utilities.getCombinedFile(currentTime, DataType.raw)
    def convert(self):
        for tweet in Utilities.iterateTweetsFromFile(self.combinedSetFile):
            pprint(tweet)
            exit()
        
class ExpertsClassifier:
    def __init__(self, numberOfExperts):
        self.numberOfExperts = numberOfExperts
        
if __name__ == '__main__':
    DocumentFormatUnigram(Settings.startTime).convert()
        
    