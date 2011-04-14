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
        self.classifierId
    def _iterateTrainingDocuments(self):
        currentTime=self.currentTime
        for i in range(self.historyLength):
            trainingFile = Utilities.getTrainingFile(currentTime, self.dataType, self.numberOfExperts)
            print trainingFile
            currentTime-=timedelta(days=1)
    def train(self):
        self._iterateTrainingDocuments()
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime, Settings.numberOfExperts, DataType.ruusl).train()  