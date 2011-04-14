'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import Settings
from datasets import DataType
from datetime import timedelta
        
class ExpertsClassifier:
    def __init__(self, currentTime, numberOfExperts, dataType, historyLength=2):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
        self.historyLength = historyLength
    def trainingDocuments(self):
        currentTime=self.currentTime
        for i in range(self.historyLength):
            trainingFile = Utilities.getTrainingFile(currentTime, self.dataType, self.numberOfExperts)
            for tweet in Utilities.iterateTweetsFromFile(trainingFile): yield tweet
            currentTime-=timedelta(days=1)
    def train(self):
        i = 1
        for tweet in self.trainingDocuments(): 
            print i, tweet['id']
            i+=1
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime+timedelta(days=1), Settings.numberOfExperts, DataType.ruusl).train()  