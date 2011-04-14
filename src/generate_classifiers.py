'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import Settings
from datasets import DataType
from datetime import timedelta
        
class ExpertsClassifier:
    def __init__(self, currentTime, numberOfExperts, dataType, historyLength=1):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
        self.historyLength = historyLength
    def _iterateTrainingDocuments(self):
        currentTime=self.currentTime
        for i in range(self.historyLength):
            trainingFile = Utilities.getTrainingFile(currentTime, self.dataType, self.numberOfExperts)
            for tweet in Utilities.iterateTweetsFromFile(trainingFile): yield tweet
            currentTime-=timedelta(days=1)
    def train(self):
        i = 1
        for tweet in self._iterateTrainingDocuments(): 
            print i, tweet['id']
            i+=1
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime, Settings.numberOfExperts, DataType.ruusl).train()  