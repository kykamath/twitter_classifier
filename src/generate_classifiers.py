'''
Created on Apr 13, 2011

@author: kykamath
'''
import cjson, numpy
import matplotlib.pyplot as plt
from settings import Settings
from datasets import DocumentType
from datetime import timedelta, datetime
from classifiers.classifiers import FixedWindowClassifier, FixedWindowWithCollocationsClassifier, TestDocuments,\
    TestDocumentsWithCollocations, FixedWindowWithRelabeledDocumentsClassifier
from utilities import Utilities
from collections import defaultdict
from collocations import Collocations

maxLength=16
idealModelLength = 8

class GenerateClassifiers:
    @staticmethod
    def fixedWindowOfDifferentLengthsAndDataTypes():
        global maxLength, idealModelLength
        dataTypes = [DocumentType.typeRuuslUnigramNounsWithMeta]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: 
                for dataType in dataTypes: FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=noOfDays).trainAndSave()
            currentDay+=timedelta(days=1)
    @staticmethod
    def fixedWindowWithCollocationsForDifferentCollocations():
        global maxLength, idealModelLength
        dataType = DocumentType.typeRuuslUnigram
        collocationMeasures = [Collocations.measureTypeLikelihoodRatio, Collocations.measureTypeRawFrequency, Collocations.measureTypePMI]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: 
                for collocationMeasure in collocationMeasures: FixedWindowWithCollocationsClassifier(collocationMeasure=collocationMeasure, currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=noOfDays).trainAndSave()
            currentDay+=timedelta(days=1)
    @staticmethod
    def fixedWindowByRelabelingDocuments():
        global maxLength, idealModelLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: FixedWindowWithRelabeledDocumentsClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays).trainAndSave()
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
                Utilities.writeAsJsonToFile(data, Settings.stats_to_determine_fixed_window_length)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsForDiminishingAUCM():
        currentDay = datetime(2011, 4, 1)
        testDay = currentDay+timedelta(days=1)
        noOfDays = [1, 8, 14]
        for daysInFuture in range(1, 11):
            for noOfDay in noOfDays:
                classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDay)
                classifier.load()
                data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'test_day': datetime.strftime(testDay, Settings.twitter_api_time_format), 'classifier_length': noOfDay, 'metric': 'accuracy', 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1, 'no_of_days_in_future': daysInFuture}
                data['value'] = classifier.getAccuracy(TestDocuments(currentTime=testDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
                Utilities.writeAsJsonToFile(data, Settings.stats_for_diminishing_aucm)
            testDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsToCompareDifferentDocumentTypes():
        global maxLength, idealModelLength
        dataTypes = [DocumentType.typeRuuslUnigram, DocumentType.typeCharBigram, DocumentType.typeCharTrigram, DocumentType.typeRuuslBigram, DocumentType.typeRuuslTrigram, DocumentType.typeRuuslSparseBigram,
                     DocumentType.typeRuuslUnigramNouns, DocumentType.typeRuuslUnigramWithMeta, DocumentType.typeRuuslUnigramNounsWithMeta]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            for noOfDays in noOfDaysList: 
                for dataType in dataTypes:
                    print currentDay, noOfDays, dataType
                    classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=noOfDays)
                    classifier.load()
                    data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': dataType, 'test_data_days': 1}
                    data['value'] = classifier.getAUCM(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=1).iterator())
                    Utilities.writeAsJsonToFile(data, Settings.stats_to_compare_different_document_types)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsToCompareCollocations():
        global maxLength, idealModelLength
        dataType = DocumentType.typeRuuslUnigram
        collocationMeasures = [Collocations.measureTypeChiSquare, Collocations.measureTypeLikelihoodRatio, Collocations.measureTypeRawFrequency, Collocations.measureTypePMI]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: 
                for collocationMeasure in collocationMeasures: 
                    classifier = FixedWindowWithCollocationsClassifier(collocationMeasure=collocationMeasure, currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=noOfDays)
                    classifier.load()
                    data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': dataType, 'collocation_measure': collocationMeasure, 'test_data_days': 1}
                    data['value'] = classifier.getAUCM(TestDocumentsWithCollocations(collocationMeasure, currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=dataType, noOfDays=1).iterator())
                    Utilities.writeAsJsonToFile(data, Settings.stats_to_compare_collocations)
            currentDay+=timedelta(days=1)
            
    @staticmethod
    def generateStatsObservePerformanceByRelabelingDocuments():
        global maxLength, idealModelLength
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            for noOfDays in noOfDaysList: 
                classifier = FixedWindowWithRelabeledDocumentsClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays)
                classifier.load()
                data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1}
                data['value'] = classifier.getAUCM(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
                print data
#                    Utilities.writeAsJsonToFile(data, Settings.stats_to_compare_different_document_types)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def analyzeStatsToDetermineFixedWindowLength():
        classifierLengthToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_determine_fixed_window_length): classifierLengthToScore[data['classifier_length']].append(data['value'])
        dataX, dataY = [], []
        for classifierLength in classifierLengthToScore: dataX.append(classifierLength), dataY.append(numpy.mean(classifierLengthToScore[classifierLength]))
        plt.plot(dataX, dataY, 'om-', lw=2)
        plt.ylabel('AUCM value')
        plt.xlabel('Length of training window (days)')
        plt.ylim( (0.2, 1) ) 
        plt.show()
    
    @staticmethod
    def analyzeStatsToCompareDifferentDocumentTypes():
        '''
        char_bigram 0.67
        ruusl_unigram_with_meta 0.71
        ruusl_bigram 0.49
        ruusl_unigram_nouns_with_meta 0.66
        ruusl_sparse_bigram 0.54
        char_trigram 0.71
        ruusl_trigram 0.00
        removed_url_users_specialcharaters_and_lemmatized 0.71
        ruusl_unigram_nouns 0.66
        '''
        languageModelToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_compare_different_document_types): languageModelToScore[data['data_type']].append(data['value'])
        for languageModel in languageModelToScore: print languageModel, '%0.2f'%numpy.mean(languageModelToScore[languageModel])
    
    @staticmethod
    def analyzeStatsToCompareCollocations():
        languageModelToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_compare_collocations): languageModelToScore[data['collocation_measure']].append(data['value'])
        for languageModel in languageModelToScore: print languageModel, numpy.mean(languageModelToScore[languageModel])
        
if __name__ == '__main__':
#    GenerateClassifiers.fixedWindowOfDifferentLengthsAndDataTypes()
#    GenerateClassifiers.fixedWindowWithCollocationsForDifferentCollocations()
#    GenerateClassifiers.fixedWindowByRelabelingDocuments()
   
#    AnalyzeClassifiers.generateStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.generateStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.generateStatsToCompareCollocations()
#    AnalyzeClassifiers.generateStatsObservePerformanceByRelabelingDocuments()
    AnalyzeClassifiers.generateStatsForDiminishingAUCM()

#    AnalyzeClassifiers.analyzeStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.analyzeStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.analyzeStatsToCompareCollocations()