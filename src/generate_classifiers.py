'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import Settings
from datasets import DataType
#from settings import DataType, Settings
#import pprint

        
class ExpertsClassifier:
    def __init__(self, currentTime, numberOfExperts, dataType):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
    def train(self):
        trainingFile = Utilities.getTrainingFile(self.currentTime, self.dataType, self.numberOfExperts)
        print trainingFile
    
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime, Settings.numberOfExperts, DataType.ruusl).train()  