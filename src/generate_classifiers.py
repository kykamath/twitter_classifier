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
    def __init__(self, currentTime, numberOfExperts, dataType, historyLength=1):
        super(ExpertsClassifier, self).__init__()
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
        self.historyLength = historyLength
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(currentTime, dataType, numberOfExperts, historyLength)
    def trainingDocuments(self):
        currentTime=self.currentTime
        for i in range(self.historyLength):
            trainingFile = Utilities.getTrainingFile(currentTime, self.dataType, self.numberOfExperts)
            for tweet in Utilities.iterateTweetsFromFile(trainingFile): yield (tweet['document'], tweet['class'])
            currentTime-=timedelta(days=1)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
        for t in self.trainingDocuments(): print t['class']
        exit()
        self.trainClassifier([t for t in self.trainingDocuments()])
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
    def load(self):
        self.classifier = Classifier.loadClassifier(self.trainedClassifierFile)

class TestDocuments:
    def __init__(self, currentTime, numberOfExperts, dataType, historyLength=1):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.dataType = dataType
        self.historyLength = historyLength
    @staticmethod
    def getTestDocuments():
        pass
        
if __name__ == '__main__':
    ExpertsClassifier(Settings.startTime+timedelta(days=1), Settings.numberOfExperts, DataType.ruusl, historyLength=2).trainAndSave()  
