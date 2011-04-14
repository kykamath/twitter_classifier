'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import DataType, Settings
import pprint
class DocumentFormatUnigram(object):
    keys = ['class', 'text', 'created_at', 'id']
    def __init__(self, currentTime):
        self.currentTime = currentTime
        self.combinedSetFile = Utilities.getCombinedFile(currentTime, DataType.raw)
    def convert(self):
        for tweet in Utilities.iterateTweetsFromFile(self.combinedSetFile):
            data = {}
            for k in DocumentFormatUnigram.keys: data[k]=tweet[k]
            data['screen_name'] = tweet['user']['screen_name']; data['user_id'] = tweet['user']['id_str']
            pprint.pprint(data)
            exit()
        
class ExpertsClassifier:
    def __init__(self, numberOfExperts):
        self.numberOfExperts = numberOfExperts
        
if __name__ == '__main__':
    DocumentFormatUnigram(Settings.startTime).convert()
        
    