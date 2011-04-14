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
    def __init__(self, **kwargs):
#        ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=1)
        super(ExpertsClassifier, self).__init__()
        self.kwargs=kwargs
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(**kwargs)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
#        for t in Utilities.getDocuments(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs): print t[1]
#        exit()
        self.trainClassifier([t for t in Utilities.getDocuments(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs)])
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
    def load(self):
        self.classifier = Classifier.loadClassifier(self.trainedClassifierFile)

class TestDocuments:
    def __init__(self, **kwargs): self.kwargs=kwargs
    def iterate(self):
        return Utilities.getDocuments(fileNameMethod=Utilities.getTestFile, dataDirection=DataDirection.future, bottom=True, **self.kwargs)
        
if __name__ == '__main__':
#    ExpertsClassifier(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=2).trainAndSave()  
    i = 1
    for d in TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=4).iterate():
        print i, d[1]
        i+=1
