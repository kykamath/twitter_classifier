'''
Created on Apr 13, 2011

@author: kykamath
'''
from utilities import Utilities
from settings import Settings
from datasets import DataType, DataDirection
from datetime import timedelta
from classes import Classifier

class ExpertsClassifier(Classifier):
#        ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=1)
    def __init__(self, **kwargs):
        super(ExpertsClassifier, self).__init__()
        self.kwargs=kwargs
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(**kwargs)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
#        for t in Utilities.getDocuments(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs): print t[1]
#        exit()
        self.trainClassifier(Utilities.getDocuments(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs))
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
    def load(self): self.classifier = Classifier.loadClassifier(self.trainedClassifierFile)

class TestDocuments:
#    TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=4)
    def __init__(self, **kwargs): self.kwargs=kwargs
    def iterator(self):
        return Utilities.getDocuments(fileNameMethod=Utilities.getTestFile, dataDirection=DataDirection.future, bottom=True, **self.kwargs)

def gen(): 
    for r in range(10): yield r

if __name__ == '__main__':
#    ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1).trainAndSave()
    
    classifier = ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1)
    classifier.load()
    print 'today:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1).iterator())
    print 'future:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1).iterator())