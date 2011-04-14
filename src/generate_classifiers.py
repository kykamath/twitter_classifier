'''
Created on Apr 13, 2011

@author: kykamath
'''
from settings import Settings
from datasets import DataType
from datetime import timedelta
from classifiers import ExpertsClassifier, TestDocuments



if __name__ == '__main__':
#    ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1).trainAndSave()
    classifier = ExpertsClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1)
    classifier.load()
    print 'today:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())
    print 'future:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())