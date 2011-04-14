'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import Settings
from datasets import DataType
from datetime import timedelta
from classes import Classifier
        
class ExpertsClassifier(Classifier):
    def __init__(self, currentTime, numberOfExperts, dataType, historyLength=2):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
        self.historyLength = historyLength
    def trainingDocuments(self):
        currentTime=self.currentTime
        for i in range(self.historyLength):
            trainingFile = Utilities.getTrainingFile(currentTime, self.dataType, self.numberOfExperts)
            for tweet in Utilities.iterateTweetsFromFile(trainingFile): yield (tweet['document'], tweet['class'])
            currentTime-=timedelta(days=1)
    def train(self):
        self.trainClassifier(self.trainingDocuments())
        
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime, Settings.numberOfExperts, DataType.ruusl).train()  