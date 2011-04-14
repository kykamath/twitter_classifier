'''
Created on Apr 13, 2011

@author: kykamath
'''
from settings import Settings
from datasets import DataType
from datetime import timedelta
from classifiers import FixedWindowClassifier, TestDocuments


class GenerateClassifiers:
    @staticmethod
    def fixedWindowOfDifferentLengths(maxLength=16):
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            classifierLengths = [1]+range(2,min([maxLength, (currentDay-Settings.startTime).days+2]),2)
            print currentDay, classifierLengths
            currentDay+=timedelta(days=1)
    

if __name__ == '__main__':
#    FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).trainAndSave()
#    classifier = FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1)
#    classifier.load()
#    print 'today:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())
#    print 'future:', classifier.getAccuracy(TestDocuments(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())

    GenerateClassifiers.fixedWindowOfDifferentLengths()