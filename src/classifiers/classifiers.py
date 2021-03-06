'''
Created on Mar 18, 2011

@author: kykamath
'''
import sys
from relabel_documents import ReLabelTrainingDocuments
sys.path.append('../')
from collections import defaultdict
from settings import Settings
from utilities import Utilities
from nltk.classify.maxent import MaxentClassifier
import numpy
from numpy import *
from scipy import *
from scipy.stats import mode
from scipy.misc.common import factorial
import cPickle
from datasets import DataDirection
from classification_evaluation_metrics import ClassificationEvaluationMetrics
from collocations import Collocations

classToIntMap = {'sports': 1, 'politics': 2, 'entertainment': 3, 'technology': 4}

class Evaluation:
    accuracy = 'accuracy'
    aucm = 'aucm'
    
class MultiClassAUC:
    def __init__(self, distributionList):
        self.c = len(distributionList[0][2])
        self.distributionList = distributionList
    def getMRevised(self):
        trueItemsCount = [[0.0 for i in range(self.c)] for j in range(self.c)]
        totalComparisons = [[0.0 for i in range(self.c)] for j in range(self.c)]
        for item in self.distributionList:
            id, j, distribution = item
            for i in [i for i in distribution if i!=j]:
                if distribution[i] < distribution[j]: 
                    trueItemsCount[i-1][j-1]+=1
                totalComparisons[i-1][j-1]+=1
        initialProbability = [[0.0 for i in range(self.c)] for j in range(self.c)]
        for i, j in [(i, j) for i in range(self.c) for j in range(self.c)]: 
            if totalComparisons[i][j] > 0: initialProbability[i][j] = trueItemsCount[i][j]/totalComparisons[i][j]
        finalProbability = [[0.0 for i in range(self.c)] for j in range(self.c)]
        for i, j in [(i, j) for i in range(self.c) for j in range(self.c) if i < j]: 
            finalProbability[i][j] = (initialProbability[i][j]+initialProbability[j][i])/2
        totalA = 0
        for i, j in [(i, j) for i in range(self.c) for j in range(self.c) if i < j]: totalA+=finalProbability[i][j]
        return 2*totalA/(self.c*(self.c-1))

class Classifier(object):
    typeFixedWindow = 'fixed_window'
    typeFixedWindowWithCollocations = 'fixed_window_with_collocations'
    typeFixedWindowWithRelabeledDocuments = 'fixed_window_with_relabeled_documents'
    typeGlobalClassifier = 'global_classifier'
    
    def __init__(self): 
        self.nltkClassifier = MaxentClassifier
        self.classifier = None
    @staticmethod
    def extractFeatures(data):
        features = {}
        for d in data: features[d] = True
        return features
    def trainClassifier(self, documents):
        from nltk.classify import apply_features
        trainSet = apply_features(Classifier.extractFeatures, list(documents))
        self.classifier = self.nltkClassifier.train(trainSet)
    def getAccuracy(self, documents):
        from nltk.classify import apply_features
        from nltk.classify.util import accuracy
        testSet = apply_features(Classifier.extractFeatures, list(documents))
        return accuracy(self.classifier, testSet)
    def classificationProbabilities(self, documents, resultsOnly = False):
        global classToIntMap
        documentSet = []
        documents = list(documents)
        for d in documents: 
            tempDict = {}
            for term in d: tempDict[term] = True
            documentSet.append(tempDict)
        pdists = self.classifier.batch_prob_classify(documentSet)
        returnPdists = []
        for pdist in pdists: 
            tempDict = {}
            [tempDict.setdefault(classToIntMap[k], pdist.prob('%s'%k)) for k in classToIntMap.keys()]
            returnPdists.append(tempDict)
        if not resultsOnly: return zip(documents, returnPdists)
        else: return returnPdists
    def getAUCM(self, documents):
        global classToIntMap
        documents = list(documents)
        documentSet = [d for d, c in documents]
        classifiedDocuments, i = [], 0
        for d, result in zip(documents, self.classificationProbabilities(documentSet, True)):
            classifiedDocuments.append((i, classToIntMap[d[1]], result))
            i+=1
        return MultiClassAUC(classifiedDocuments).getMRevised()
    def getF(self, documents):
        predicted, labels = self._getPredictedAndLabeled(documents)
        return ClassificationEvaluationMetrics.F(predicted, labels)
    def getMI(self, documents):
        predicted, labels = self._getPredictedAndLabeled(documents)
        return ClassificationEvaluationMetrics.mutual_info(predicted, labels)
    def _getPredictedAndLabeled(self, documents):
        from nltk.classify import apply_features
        documents = list(documents)
        testSet = apply_features(Classifier.extractFeatures, list(documents))
        return (array(self.classifier.batch_classify([fs for (fs,l) in testSet])), array([l for (fs,l) in documents]))
#    def evaluate(self, documents, methodology=None):
#        if methodology==None: return {Evaluation.accuracy: self.getAccuracy(documents), Evaluation.aucm: self.getAUCM(documents)}
#        elif methodology==Evaluation.accuracy: return {Evaluation.accuracy: self.getAccuracy(documents)}
#        elif methodology==Evaluation.aucm: return {Evaluation.aucm: self.getAUCM(documents)}
    def showMostInformativeFeatures(self, n = 10, show='all'):
        def getFeatureTuple(data): return (data.split('==')[0], data.split()[-1][1:-1])
        fids = sorted(range(len(self.classifier._weights)),
                      key=lambda fid: abs(self.classifier._weights[fid]),
                      reverse=True)
        if show == 'pos':
            fids = [fid for fid in fids if self.classifier._weights[fid]>0]
        elif show == 'neg':
            fids = [fid for fid in fids if self.classifier._weights[fid]<0]
#        for fid in fids[:n]: print '%8.3f %s' % (self.classifier._weights[fid], self.classifier._encoding.describe(fid))
        return [getFeatureTuple(self.classifier._encoding.describe(fid)) for fid in fids[:n]]
#        self.classifier.show_most_informative_features(n)
    @staticmethod
    def saveClassifier(classifier, fileName): 
        Utilities.createDirectory(fileName)
        cPickle.dump(classifier, open(fileName, 'w'))
    @staticmethod
    def loadClassifier(fileName): return cPickle.load(open(fileName))

class FixedWindowClassifier(Classifier):
#        FixedWindowClassifier(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, noOfDays=1)
    def __init__(self, **kwargs):
        super(FixedWindowClassifier, self).__init__()
        self.kwargs=kwargs
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(classifierType=Classifier.typeFixedWindow, **kwargs)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
        self.trainClassifier(Utilities.getTweets(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs))
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
    def load(self): self.classifier = Classifier.loadClassifier(self.trainedClassifierFile)

class FixedWindowWithCollocationsClassifier(FixedWindowClassifier):
    def __init__(self, collocationMeasure, **kwargs):
        super(FixedWindowWithCollocationsClassifier, self).__init__(**kwargs)
        self.collocationMeasure = collocationMeasure
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(classifierType=Classifier.typeFixedWindowWithCollocations+'_%s'%collocationMeasure, **kwargs)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
        collocations = Collocations(self.collocationMeasure, **self.kwargs)
        collocations.load()
        self.trainClassifier(Utilities.getTweetsWithCollocations(collocations, fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs))
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)

class FixedWindowWithRelabeledDocumentsClassifier(FixedWindowClassifier):
    def __init__(self, **kwargs): 
        super(FixedWindowWithRelabeledDocumentsClassifier, self).__init__(**kwargs)
        self.trainedClassifierFile = Utilities.getTrainedClassifierFile(classifierType=Classifier.typeFixedWindowWithRelabeledDocuments, **kwargs)
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
        self.trainClassifier(ReLabelTrainingDocuments(Utilities.getTweets(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs)).getRelabeledDocuments())
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
        
class GlobalClassifier(Classifier):
    def __init__(self, **kwargs):
        super(GlobalClassifier, self).__init__(**kwargs)
        self.trainedClassifierFile = Settings.twitterClassifierTrainedModelsFolder+'global_classifier'
    def trainAndSave(self):
        Utilities.createDirectory(self.trainedClassifierFile)
        self.trainClassifier(((d['data'], d['class'])for d in Utilities.iterateJsonFromFile(Settings.globalClassifierData)))
        Classifier.saveClassifier(self.classifier, self.trainedClassifierFile)
    def load(self): self.classifier = Classifier.loadClassifier(self.trainedClassifierFile)

class TestDocuments:
#    TestDocuments(currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DataType.ruusl, historyLength=4)
    def __init__(self, **kwargs): self.kwargs=kwargs
    def iterator(self):
        return Utilities.getTweets(fileNameMethod=Utilities.getTestFile, dataDirection=DataDirection.future, bottom=True, **self.kwargs)

class TestDocumentsWithCollocations:
    def __init__(self, collocationMeasure, **kwargs): 
        self.collocationMeasure = collocationMeasure
        self.kwargs=kwargs
    def iterator(self):
        testNoOfDays = self.kwargs['noOfDays']
        self.kwargs['noOfDays'] = 8
        collocations = Collocations(self.collocationMeasure, **self.kwargs)
        collocations.load()
        self.kwargs['noOfDays'] = testNoOfDays
        return Utilities.getTweetsWithCollocations(collocations, fileNameMethod=Utilities.getTestFile, dataDirection=DataDirection.future, bottom=True, **self.kwargs)
