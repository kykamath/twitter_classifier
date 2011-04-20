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
    def fixedWindowWithCollocationsForDifferentCollocations(numberOfExperts=Settings.numberOfExperts):
        global maxLength, idealModelLength
        dataType = DocumentType.typeRuuslUnigram
        collocationMeasures = [Collocations.measureTypeLikelihoodRatio, Collocations.measureTypeChiSquare]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: 
                for collocationMeasure in collocationMeasures: FixedWindowWithCollocationsClassifier(collocationMeasure=collocationMeasure, currentTime=currentDay, numberOfExperts=numberOfExperts, dataType=dataType, noOfDays=noOfDays).trainAndSave()
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
        currentDay = datetime(2011, 3, 26)
        for i in range(5):
            print currentDay
            try:
                testDay = currentDay+timedelta(days=1)
                noOfDays = [1, 4, 8]
                for daysInFuture in range(1, 20):
                    for noOfDay in noOfDays:
                            classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDay)
                            classifier.load()
                            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'test_day': datetime.strftime(testDay, Settings.twitter_api_time_format), 'classifier_length': noOfDay, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1, 'no_of_days_in_future': daysInFuture}
                            data['value'] = classifier.getAUCM(TestDocuments(currentTime=testDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
                            Utilities.writeAsJsonToFile(data, Settings.stats_for_diminishing_aucm)
                    testDay+=timedelta(days=1)
            except: pass
            currentDay+=timedelta(days=1)
    
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
        collocationMeasures = [Collocations.measureTypeChiSquare, Collocations.measureTypeLikelihoodRatio]
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            print currentDay, noOfDaysList
            for noOfDays in noOfDaysList: 
                for collocationMeasure in collocationMeasures: 
                    classifier = FixedWindowWithCollocationsClassifier(collocationMeasure=collocationMeasure, currentTime=currentDay, numberOfExperts=Settings.numberOfExpertsSecondSet, dataType=dataType, noOfDays=noOfDays)
                    classifier.load()
                    data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExpertsSecondSet, 'data_type': dataType, 'collocation_measure': collocationMeasure, 'test_data_days': 1}
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
                Utilities.writeAsJsonToFile(data, Settings.stats_to_observe_performance_by_relabeling_documents)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsForTopFeatures():
        global maxLength
        currentDay = Settings.startTime
        noOfDays = 1
        while currentDay<=Settings.endTime:
            classifier = FixedWindowClassifier(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays)
            classifier.load()
            classifier.showMostInformativeFeatures(100)
#            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'metric': 'aucm', 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1}
#            data['value'] = classifier.getAUCM(TestDocuments(currentTime=currentDay+timedelta(days=1), numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
#            Utilities.writeAsJsonToFile(data, Settings.stats_to_determine_fixed_window_length)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def analyzeStatsToDetermineFixedWindowLength():
        classifierLengthToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_determine_fixed_window_length): classifierLengthToScore[data['classifier_length']].append(data['value'])
        dataX, dataY = [], []
        for classifierLength in classifierLengthToScore: dataX.append(classifierLength), dataY.append(numpy.mean(classifierLengthToScore[classifierLength]))
        plt.plot(dataX, dataY, 'om-', lw=2, label='Unigram model')
        plt.legend()
        plt.title('AUCM at different model window training lengths')
        plt.ylabel('AUCM value')
        plt.xlabel('Length of training window (days)')
        plt.ylim( (0.2, 1) ) 
        plt.show()
    
    @staticmethod
    def analyzeStatsForDimnishingAUCMValues():
        daysToScore = defaultdict(dict)
        color = {1: 'rx-', 8: 'g>-', 14: 'bo-'}
        for data in Utilities.iterateJsonFromFile(Settings.stats_for_diminishing_aucm): 
            if data['no_of_days_in_future'] not in daysToScore[data['classifier_length']]: daysToScore[data['classifier_length']][data['no_of_days_in_future']]=[]
            daysToScore[data['classifier_length']][data['no_of_days_in_future']].append(data['value'])
        for classifierLength in sorted(daysToScore):
            print classifierLength
            dataX = daysToScore[classifierLength].keys()[4:9]
            dataY = [numpy.mean(daysToScore[classifierLength][x]) for x in dataX]
            plt.plot(dataX, dataY, color[classifierLength], label=str(classifierLength), lw=2)
        plt.legend()
        plt.ylabel('AUCM value')
        plt.xlabel('Number of days in future')
        plt.title('Decay in AUCM with time')
        plt.xticks( range(5,10), range(1,6) )
        plt.ylim( (0.627, 0.735) ) 
        plt.show()
        
    @staticmethod
    def analyzeStatsToCompareDifferentDocumentTypes():
        '''
        char_bigram 0.67 0.00
        ruusl_unigram_with_meta 0.71 0.00
        ruusl_bigram 0.49 0.00
        ruusl_unigram_nouns_with_meta 0.66 0.00
        ruusl_sparse_bigram 0.54 0.00
        removed_url_users_specialcharaters_and_lemmatized 0.71 0.00
        ruusl_unigram_nouns 0.66 0.00
        '''
        languageModelToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_compare_different_document_types): languageModelToScore[data['data_type']].append(data['value'])
        for languageModel in languageModelToScore: print languageModel, '%0.2f'%numpy.mean(languageModelToScore[languageModel]), '%0.2f'%numpy.var(languageModelToScore[languageModel])
    
    @staticmethod
    def analyzeStatsToCompareCollocations():
        '''
        125 chi_sqare 0.70 0.00
        125 likelihood_ratio 0.69 0.00
        375 chi_sqare 0.74 0.00
        375 likelihood_ratio 0.69 0.00
        '''
        languageModelToScore=defaultdict(list)
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_compare_collocations): languageModelToScore['%s %s'%(data['number_of_experts'], data['collocation_measure'])].append(data['value'])
        for languageModel in languageModelToScore: print languageModel, '%0.2f'%numpy.mean(languageModelToScore[languageModel]), '%0.2f'%numpy.var(languageModelToScore[languageModel])
        
    @staticmethod
    def analyzeStatsToObservePerformanceByRelabelingDocuments():
        '''
        0.67 0.00
        '''
        perfromanceByRelabeling=[]
        for data in Utilities.iterateJsonFromFile(Settings.stats_to_observe_performance_by_relabeling_documents): perfromanceByRelabeling.append(data['value'])
        print '%0.2f'%numpy.mean(perfromanceByRelabeling), '%0.2f'%numpy.var(perfromanceByRelabeling)
        
if __name__ == '__main__':
#    GenerateClassifiers.fixedWindowOfDifferentLengthsAndDataTypes()
#    GenerateClassifiers.fixedWindowWithCollocationsForDifferentCollocations(numberOfExperts=Settings.numberOfExpertsSecondSet)
#    GenerateClassifiers.fixedWindowByRelabelingDocuments()
   
#    AnalyzeClassifiers.generateStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.generateStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.generateStatsToCompareCollocations()
#    AnalyzeClassifiers.generateStatsObservePerformanceByRelabelingDocuments()
#    AnalyzeClassifiers.generateStatsForDiminishingAUCM()
    AnalyzeClassifiers.generateStatsForTopFeatures()

#    AnalyzeClassifiers.analyzeStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.analyzeStatsForDimnishingAUCMValues()
#    AnalyzeClassifiers.analyzeStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.analyzeStatsToCompareCollocations()
#    AnalyzeClassifiers.analyzeStatsToObservePerformanceByRelabelingDocuments()