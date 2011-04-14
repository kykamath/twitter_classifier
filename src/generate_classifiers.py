'''
Created on Apr 13, 2011

@author: kykamath
'''
from settings import Settings
from datasets import DataType
from datetime import timedelta
from classifiers import FixedWindowClassifier, TestDocuments
from utilities import Utilities

maxLength=16

class GenerateClassifiers:
    @staticmethod
    def fixedWindowOfDifferentLengths():
        global maxLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            for noOfDays in Utilities.getClassifierLengthsByDay(currentDay, maxLength): FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=noOfDays).trainAndSave()
            currentDay+=timedelta(days=1)

class AnalyzeClassifiers:
    @staticmethod
    def generateStatsToDetermineFixedWindowLength():
        global maxLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            for noOfDays in Utilities.getClassifierLengthsByDay(currentDay, maxLength): 
                classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=noOfDays)
                classifier.load()
                print currentDay, noOfDays, 'accuracy', classifier.getAccuracy(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())
                print currentDay, noOfDays, 'aucm', classifier.getAUCM(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())
            currentDay+=timedelta(days=1)

if __name__ == '__main__':
#    FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).trainAndSave()
#    classifier = FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1)
#    classifier.load()
#    print 'today:', classifier.getAUCM(TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())
#    print 'future:', classifier.getAUCM(TestDocuments(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DataType.typeRuusl, noOfDays=1).iterator())

#    GenerateClassifiers.fixedWindowOfDifferentLengths()
    AnalyzeClassifiers.generateStatsToDetermineFixedWindowLength()