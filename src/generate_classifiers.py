'''
Created on Apr 13, 2011

@author: kykamath
'''
import cjson
from settings import Settings
from datasets import DocumentType
from datetime import timedelta, datetime
from classifiers import FixedWindowClassifier, TestDocuments
from utilities import Utilities

maxLength=16

class GenerateClassifiers:
    @staticmethod
    def fixedWindowOfDifferentLengthsAndDataTypes():
        global maxLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
#            dataTypes = [DocumentType.typeRuuslUnigram]
#            noOfDaysList = Utilities.getClassifierLengthsByDay(currentDay, maxLength)
            dataTypes = [DocumentType.typeRuuslBigram, DocumentType.typeRuuslSparseBigram, DocumentType.typeRuuslTrigram]
            noOfDaysList = [125]
            for noOfDays in noOfDaysList: 
                for dataType in dataTypes: FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=noOfDays).trainAndSave()
            currentDay+=timedelta(days=1)

class AnalyzeClassifiers:
    @staticmethod
    def generateStatsToDetermineFixedWindowLength():
        global maxLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            for noOfDays in Utilities.getClassifierLengthsByDay(currentDay, maxLength): 
                classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays)
                classifier.load()
                data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1}
                data['value'] = classifier.getAUCM(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
                cjson.encode(data)
            currentDay+=timedelta(days=1)

if __name__ == '__main__':
#    FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuusl, noOfDays=1).trainAndSave()
#    classifier = FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuusl, noOfDays=1)
#    classifier.load()
#    print 'today:', classifier.getAUCM(TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuusl, noOfDays=1).iterator())
#    print 'future:', classifier.getAUCM(TestDocuments(currentTime=Settings.startTime+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuusl, noOfDays=1).iterator())

#    GenerateClassifiers.fixedWindowOfDifferentLengths()
    AnalyzeClassifiers.generateStatsToDetermineFixedWindowLength()