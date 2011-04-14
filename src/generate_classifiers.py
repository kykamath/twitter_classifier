'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import DataType, Settings
import pprint
class DocumentFormat(object):
    keys = ['class', 'text', 'created_at', 'id']
    numberOfExperts = 250
    def __init__(self, currentTime, outputDataType):
        self.currentTime = currentTime
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DataType.raw, DocumentFormat.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DataType.raw, DocumentFormat.numberOfExperts)
        self.outputTrainingSetFile = Utilities.getTrainingFile(currentTime, outputDataType, DocumentFormat.numberOfExperts)
        self.outputTestSetFile = Utilities.getTestFile(currentTime, outputDataType, DocumentFormat.numberOfExperts)
    def convert(self):
        for tweet in Utilities.iterateTweetsFromFile(self.inputTrainingSetFile):
            data = {}
            for k in DocumentFormat.keys: data[k]=tweet[k]
            data['screen_name'] = tweet['user']['screen_name']; data['user_id'] = tweet['user']['id_str']
            data['document'] = self.modifyDocument(data['text'])
            pprint.pprint(data)
            exit()

class DocumentFormatRawUnigram(DocumentFormat):
    def __init__(self, currentTime): super(DocumentFormatRawUnigram, self).__init__(currentTime, DataType.raw_unigram)
    def modifyDocument(self, text): return text.strip().lower().split()
        
class ExpertsClassifier:
    def __init__(self, numberOfExperts):
        self.numberOfExperts = numberOfExperts
        
if __name__ == '__main__':
    DocumentFormatRawUnigram(Settings.startTime).convert()
        
    