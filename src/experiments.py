'''
Created on Apr 13, 2011

@author: kykamath
'''
import cjson, numpy
import matplotlib.pyplot as plt
from settings import Settings
from datasets import DocumentType, DataDirection, CreateTrainingAndTestSets
from datetime import timedelta, datetime
from classifiers.classifiers import FixedWindowClassifier, FixedWindowWithCollocationsClassifier, TestDocuments,\
    TestDocumentsWithCollocations, FixedWindowWithRelabeledDocumentsClassifier,\
    GlobalClassifier
from utilities import Utilities, ExpertUsers
from collections import defaultdict
from collocations import Collocations
from itertools import groupby
from operator import itemgetter
from matplotlib import mpl
from matplotlib.dates import drange
from classifiers.stream_classifier import StreamClassifierNaiveBayesWithLaplaceSmoothing,\
    StreamClassifierFeatureScoreDecay,\
    StreamClassifierFeatureScoreDecayWithInverseClassFrequency

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
    @staticmethod
    def globalClassifier():
        classifier = GlobalClassifier()
        classifier.trainAndSave()

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
            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classifier_length': noOfDays, 'number_of_experts': Settings.numberOfExperts, 'data_type': DocumentType.typeRuuslUnigram}
            data['features']=classifier.showMostInformativeFeatures(2000)
            Utilities.writeAsJsonToFile(data, Settings.stats_for_most_informative_features)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsForTrainingDataPerDay():
        currentDay = Settings.startTime
        noOfDays = 1
        while currentDay<=Settings.endTime:
            classDistribution = defaultdict(int)
            for d in Utilities.getTweets(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays):
                classDistribution[d[1]]+=1
            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'class_distribution': classDistribution}
            Utilities.writeAsJsonToFile(data, Settings.stats_for_training_data)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsForGlobalClassifier():
        classifier = GlobalClassifier()
        classifier.load()
        currentDay = Settings.startTime
        while currentDay<=Settings.endTime:
            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format),  'metric': 'aucm', 'data_type': DocumentType.typeRuuslUnigram, 'test_data_days': 1}
            data['value'] = classifier.getAUCM(TestDocuments(currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).iterator())
            Utilities.writeAsJsonToFile(data, Settings.stats_for_global_classifier)
            currentDay+=timedelta(days=1)
        
    @staticmethod
    def generateDataSetStats():
        currentDay = Settings.startTime
        expertUsers = ExpertUsers()
        allExpertsList={}
        for k, v in expertUsers.list.iteritems(): allExpertsList[k]=v
        while currentDay<=Settings.endTime:
            data = {'day': datetime.strftime(currentDay, Settings.twitter_api_time_format), 'classes': defaultdict(int), 'total_tweets': 0}
            for tweet in CreateTrainingAndTestSets.getTweetsFromExperts(allExpertsList, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentDay)):
                if tweet['user']['id_str'] in expertUsers.list: 
                    classType = allExpertsList[tweet['user']['id_str']]['class']
                    data['classes'][classType]+=1
                    data['total_tweets']+=1
            Utilities.writeAsJsonToFile(data, Settings.stats_for_dataset)
            currentDay+=timedelta(days=1)
    
    @staticmethod
    def generateStatsForStreamClassifier():
        streamClassifiers = [StreamClassifierFeatureScoreDecay, StreamClassifierFeatureScoreDecayWithInverseClassFrequency, StreamClassifierNaiveBayesWithLaplaceSmoothing]
        numberOfExpertsList = [Settings.numberOfExperts]
        noOfDaysList = [25]
        score_thresholds = [0.2*i for i in range(5)]
        for classifier in streamClassifiers:
            for numberOfExperts in numberOfExpertsList:
                for noOfDays in noOfDaysList:
                    for score_threshold in score_thresholds:
                        Settings.stream_classifier_class_probability_threshold = score_threshold
                        streamClassifier = classifier(decayRate=Settings.stream_classifier_decay_rate, currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=numberOfExperts, noOfDays=noOfDays)
                        streamClassifier.classifyingMethod = streamClassifier.classifyForAUCM
                        data = {'classifier_type':streamClassifier.type, 'stream_length_in_days':noOfDays, 'number_of_experts': numberOfExperts, 'metric':'aucm', 'score_threshold':Settings.stream_classifier_class_probability_threshold}
                        streamClassifier.start()
                        data['number_of_documents_classified'] = len(streamClassifier.classifiedDocuments)
                        data['value']=streamClassifier.getAUCM()
                        Utilities.writeAsJsonToFile(Settings.stream_classifier_class_probability_threshold, Settings.stats_for_stream_classifier_comparisons)
    
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
    
    @staticmethod
    def _getFeatureDataByDay():
        dataByDay = defaultdict(dict)
        for l in Utilities.iterateJsonFromFile(Settings.stats_for_most_informative_features):
            day = datetime.strptime(l['day'], Settings.twitter_api_time_format)
            for k, g in groupby(sorted(l['features'], key=itemgetter(1)), key=itemgetter(1)): dataByDay[day][k] = [i[0] for i in g]
        return dataByDay
    
    @staticmethod
    def analyzeStatsForTopFeaturesFeatureChange():
        yticks = ('sports', 'technology', 'entertainment', 'politics')
        dataByDay = AnalyzeClassifiers._getFeatureDataByDay()
        changeInFeatures = defaultdict(dict)
        previousDaysData = None
        for k in sorted(dataByDay):
            if previousDaysData==None: previousDaysData=dataByDay[k]
            else:
                currentDaysData = dataByDay[k]
                for classType in currentDaysData:
                    currentDaysFeatureSet = set(currentDaysData[classType][:100])
                    previousDaysFeatureSet = set(previousDaysData[classType][:100])
                    changeInFeatures[k][classType]=(len(currentDaysFeatureSet.union(previousDaysFeatureSet))-len(currentDaysFeatureSet.intersection(previousDaysFeatureSet)))/float(len(previousDaysFeatureSet))
        dataToPlot = defaultdict(list)
        cmap = mpl.cm.Blues
        fig=plt.figure()
        for k in sorted(changeInFeatures): [dataToPlot[classType].append(changeInFeatures[k][classType])for classType in changeInFeatures[k]]
        plt.imshow([dataToPlot[k] for k in yticks], cmap = cmap, interpolation='nearest', aspect=5, alpha=1, vmin=1.4, vmax=1.7)
        plt.xticks(())
        plt.yticks(range(len(yticks)), yticks)
        plt.xlabel('March-April 2011')
        plt.title('Ratio of feature change')
        ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
        norm = mpl.colors.Normalize(vmin=1.4, vmax=1.7)
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                       norm=norm,
                                       orientation='vertical',alpha=1)
        
        plt.show()
    
    @staticmethod
    def analyzeStatsForConceptDriftExamples():
        featuresToPlot = ['mlb', 'espn', 'sfgiants', 'butler', 'nhl']
        dataByDay = AnalyzeClassifiers._getFeatureDataByDay()
        classType = 'sports'
        featureRankMap = defaultdict(dict)
        for d in sorted(dataByDay):
            for feature in dataByDay[d][classType][:20]: featureRankMap[feature][d]=dataByDay[d][classType].index(feature)+1
#        for feature in featureRankMap:
#            if len(featureRankMap[feature]) >3: print feature, featureRankMap[feature]
        dataToPlot = defaultdict(list)
        for d in sorted(dataByDay):
            for feature in featureRankMap:
                if len(featureRankMap[feature])>3:
                    dataToPlot[feature].append(featureRankMap[feature].get(d, 25))
        for f in dataToPlot: print f, dataToPlot[f]
        cmap = mpl.cm.gray
        fig=plt.figure()
        plt.imshow([dataToPlot[k] for k in featuresToPlot], cmap = cmap, interpolation='nearest', aspect=5, alpha=2)
        plt.xticks(())
        plt.yticks(range(len(featuresToPlot)), [k for k in featuresToPlot])
        plt.xlabel('March-April 2011')
        plt.title('Changing concepts in sports')
        ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
        norm = mpl.colors.Normalize(vmin=1, vmax=20)
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                           norm=norm,
                                           orientation='vertical',alpha=1)
        plt.show()
    
    @staticmethod
    def analyzeTrainingData():
        yticks = ('sports', 'technology', 'entertainment', 'politics')
        dataByDay = {}
        for l in Utilities.iterateJsonFromFile(Settings.stats_for_training_data):
            dataByDay[datetime.strptime(l['day'], Settings.twitter_api_time_format)] = l['class_distribution']
        dataToPlot = defaultdict(list)
        previousDaysData = None
        for d in sorted(dataByDay):
            if previousDaysData==None: previousDaysData=dataByDay[d]
            else:
                currentDaysData = dataByDay[d]
                for classType in currentDaysData:
                    dataToPlot[classType].append(numpy.sqrt((currentDaysData[classType]-previousDaysData[classType])**2)/previousDaysData[classType])
        fig=plt.figure()
        cmap=mpl.cm.Blues
        for k in dataToPlot: print k, dataToPlot[k]
        plt.imshow([dataToPlot[k] for k in yticks], cmap = cmap, interpolation='nearest', aspect=5, alpha=1, vmin=0, vmax=2)
        plt.xticks(())
        plt.yticks(range(len(yticks)), [k for k in yticks])
        plt.xlabel('March-April 2011')
        plt.title('Ratio of change in training-set size.')
        
        ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
        norm = mpl.colors.Normalize(vmin=0, vmax=2)
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                       norm=norm,
                                       orientation='vertical',alpha=1)
        
        plt.show()
        
    @staticmethod
    def analyzeStatsForGlobalClassifier():
        dataToPlot=dict()
        for l in Utilities.iterateJsonFromFile(Settings.stats_for_global_classifier): dataToPlot[datetime.strptime(l['day'], Settings.twitter_api_time_format)]=l['value']
        
        date1 = Settings.startTime
        date2 = Settings.endTime
        dates = drange(date1, date2, timedelta(days=1))
        
        print len(dates), len(dataToPlot)
        fig=plt.figure()
#        plt.plot_date(dates, [1 for k in dates], '-')
        plt.plot_date(dates, [dataToPlot[k] for k in sorted(dataToPlot)[:-1]], 'g-', lw=2, label='Global classifier (mean:%0.2f)'%numpy.mean(dataToPlot.values()))
#        plt.plot_date(dates, [0 for k in dates], '-')
        plt.ylim((0.4,0.55))
        plt.ylabel('AUCM value')
        plt.xlabel('Day')
        plt.title('AUCM values for global classifier.')
        plt.legend()
        fig.autofmt_xdate()
        plt.show()
        
    @staticmethod
    def analyzeStatsForDatasets():
        '''
        1253451
        politics 325699 13027.96
        entertainment 222124 8884.96
        technology 372908 14916.32
        sports 332720 13308.8
        25
        '''
        total, perClassCount = 0, {}
        for l in Utilities.iterateJsonFromFile(Settings.stats_for_dataset):
            total+=l['total_tweets']
            for classType in l['classes']:
                if classType not in perClassCount: perClassCount[classType]={'total':0, 'no_of_days':0}
                perClassCount[classType]['total']+=l['classes'][classType]
                perClassCount[classType]['no_of_days']+=1
        print total
        for k, v in perClassCount.iteritems(): print k, perClassCount[k]['total'], perClassCount[k]['total']/float(perClassCount[k]['no_of_days'])
        print perClassCount[k]['no_of_days']
        
if __name__ == '__main__':
#    GenerateClassifiers.fixedWindowOfDifferentLengthsAndDataTypes()
#    GenerateClassifiers.fixedWindowWithCollocationsForDifferentCollocations(numberOfExperts=Settings.numberOfExpertsSecondSet)
#    GenerateClassifiers.fixedWindowByRelabelingDocuments()
#    GenerateClassifiers.globalClassifier()
    
#    AnalyzeClassifiers.generateStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.generateStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.generateStatsToCompareCollocations()
#    AnalyzeClassifiers.generateStatsObservePerformanceByRelabelingDocuments()
#    AnalyzeClassifiers.generateStatsForDiminishingAUCM()
#    AnalyzeClassifiers.generateStatsForTopFeatures()
#    AnalyzeClassifiers.generateStatsForTrainingDataPerDay()
#    AnalyzeClassifiers.generateStatsForGlobalClassifier()
#    AnalyzeClassifiers.generateDataSetStats()
    AnalyzeClassifiers.generateStatsForStreamClassifier()
    
#    AnalyzeClassifiers.analyzeStatsToDetermineFixedWindowLength()
#    AnalyzeClassifiers.analyzeStatsForDimnishingAUCMValues()
#    AnalyzeClassifiers.analyzeStatsToCompareDifferentDocumentTypes()
#    AnalyzeClassifiers.analyzeStatsToCompareCollocations()
#    AnalyzeClassifiers.analyzeStatsToObservePerformanceByRelabelingDocuments()
#    AnalyzeClassifiers.analyzeStatsForTopFeaturesFeatureChange()
#    AnalyzeClassifiers.analyzeStatsForConceptDriftExamples()
#    AnalyzeClassifiers.analyzeTrainingData()
#    AnalyzeClassifiers.analyzeStatsForGlobalClassifier()
#    AnalyzeClassifiers.analyzeStatsForDatasets()