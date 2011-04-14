'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
from settings import Settings
from utilities import Utilities
from nltk.classify.maxent import MaxentClassifier
import cPickle

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
        trainSet = apply_features(Classifier.extractFeatures, documents)
        self.classifier = self.nltkClassifier.train(trainSet)
    def testClassifier(self, documents):
        from nltk.classify import apply_features
        from nltk.classify.util import accuracy
        testSet = apply_features(Classifier.extractFeatures, documents)
        return accuracy(self.classifier, testSet)
    def classificationProbabilities(self, documents, resultsOnly = False):
        documentSet = []
        for d in documents: 
            tempDict = {}
            for term in d: tempDict[term] = True
            documentSet.append(tempDict)
        pdists = self.classifier.batch_prob_classify(documentSet)
        returnPdists = []
        for pdist in pdists: 
            tempDict = {}
            [tempDict.setdefault(k, pdist.prob('%s'%k)) for k in [1, 2, 3, 4, 5, 6]]
            returnPdists.append(tempDict)
        if not resultsOnly: return zip(documents, returnPdists)
        else: return returnPdists
    def getAUCM(self, documents):
        documentSet = [d for d, c in documents]
        classifiedDocuments, i = [], 0
        for d, result in zip(documents, self.classificationProbabilities(documentSet, True)):
            classifiedDocuments.append((i, int(d[1]), result))
            i+=1
        return MultiClassAUC(classifiedDocuments).getMRevised()
    def evaluate(self, documents, methodology=None):
        if methodology==None: return {Evaluation.accuracy: self.testClassifier(documents), Evaluation.aucm: self.getAUCM(documents)}
        elif methodology==Evaluation.accuracy: return {Evaluation.accuracy: self.testClassifier(documents)}
        elif methodology==Evaluation.aucm: return {Evaluation.aucm: self.getAUCM(documents)}
    @staticmethod
    def saveClassifier(classifier, fileName): 
        Utilities.createDirectory(fileName)
        cPickle.dump(classifier, open(fileName, 'w'))
    @staticmethod
    def loadClassifier(fileName): return cPickle.load(open(fileName))
