'''
Created on Apr 17, 2011

@author: kykamath
'''
import sys, math
sys.path.append('../')
from datasets import DataDirection, DocumentType, TweetType
from utilities import Utilities
from settings import Settings
from datetime import datetime, timedelta
from collections import defaultdict
from operator import itemgetter
from classifiers import classToIntMap, MultiClassAUC

class FeatureScore:
    def __init__(self):
        self.score = 0
        self.lastUpdateTime = None
    def update(self, decayRate, newTime, increaseValue):
        if self.lastUpdateTime==None: self.score=increaseValue
        else: self.score= self.score*math.pow(decayRate, ((newTime-self.lastUpdateTime).seconds)/3600)+increaseValue
        self.lastUpdateTime=newTime

class StreamClassifier(object):
    typeDefault='stream_classifier_default'
    
    notClassified = 'not_classified'
    numberOfClasses = 4
    
    def __init__(self, numberOfInitialBufferDays=1, classifyingMethod=None, **kwargs):
        self.featureMap = {}
        self.numberOfInitialBufferDays = numberOfInitialBufferDays
        self.classifyingMethod = classifyingMethod
        if self.classifyingMethod==None: self.classifyingMethod = self.classify
        self.kwargs = kwargs
        self.numberOfTestTweets, self.classifiedDocuments = 0, []
    def start(self):
        i=1
        firstDay = Settings.startTime+timedelta(days=self.numberOfInitialBufferDays)
        for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **self.kwargs):
            tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
            if tweet['tweet_type'] == TweetType.train: self.learnFromTweet(tweet)
            else:
                if firstDay<tweetTimeStamp: 
#                    self.classifyTweet(tweet)
                    self.classifyingMethod(tweet, self.classifyTweet(tweet))
#                    print i, self.classifyingMethod(tweet, self.classifyTweet(tweet)), tweet['class'], tweet['text']
#                    if i==25: 
#                        print self.getAUCM()
#                        exit()
#                    i+=1
    def classify(self, tweet, perClassScores):
        sortedScores = sorted(perClassScores.iteritems(), key=itemgetter(1), reverse=True)
        if sortedScores: return sortedScores[0][0]
        return StreamClassifier.notClassified
    def classifyForAUCM(self, tweet, perClassScores):
        tempDict = {}
        if perClassScores:
            sortedScores = sorted(perClassScores.iteritems(), key=itemgetter(1), reverse=True)
            if sortedScores[0][1]>=math.log(Settings.stream_classifier_class_probability_threshold):
                for classLabel, classId in classToIntMap.iteritems():
                    if classLabel not in perClassScores: tempDict[classId]=None
                    else: tempDict[classId]=perClassScores[classLabel]
                self.classifiedDocuments.append((self.numberOfTestTweets, classToIntMap[tweet['class']], tempDict))
                self.numberOfTestTweets+=1
    def getFeatureProbabilites(self, feature, tweetTime):
        mapToReturn = {}
        totalScore = 0
        for featureScore in feature['class'].itervalues(): 
            featureScore.update(self.decayRate, tweetTime, 0)
            totalScore+=featureScore.score
        for classLabel, featureScore in feature['class'].iteritems(): mapToReturn[classLabel] = float(featureScore.score)/totalScore
        return mapToReturn
    def getAUCM(self): return MultiClassAUC(self.classifiedDocuments).getMRevised()
    @staticmethod
    def extractFeatures(document):
        for feature in document:
            if feature not in Utilities.stopwords: yield feature

class StreamClassifierWithDecay(StreamClassifier):
    def __init__(self, decayRate, **kwargs):
        super(StreamClassifierWithDecay, self).__init__(**kwargs)
        self.decayRate=decayRate
    def learnFromTweet(self, tweet):
        classLabel = tweet['class']
        tweetTime = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
        for feature in StreamClassifier.extractFeatures(tweet['document']):
            if feature not in self.featureMap: self.featureMap[feature] = {'stats': {}, 'class': defaultdict(FeatureScore)}
            self.featureMap[feature]['class'][classLabel].update(self.decayRate, tweetTime, 1)
    def classifyTweet(self, tweet):
        tweetFeatureMap = {}
        tweetTime = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
        for feature in StreamClassifier.extractFeatures(tweet['document']):
            if feature in self.featureMap: tweetFeatureMap[feature]=self.getFeatureProbabilites(self.featureMap[feature], tweetTime)
        perClassScores = defaultdict(float)
        for k, v in tweetFeatureMap.iteritems(): 
            featureScore = math.log(float(StreamClassifier.numberOfClasses)/len(v))
            if featureScore!=0:
                for classLabel, score in v.iteritems(): perClassScores[classLabel]+=math.log(featureScore*score)
        return perClassScores

#class StreamClassifierWithDecayWithFeaturePriorities(StreamClassifierWithDecay):
#    def __init__(self, decayRate, **kwargs):
#        super(StreamClassifierWithDecayWithFeaturePriorities, self).__init__(decayRate, **kwargs)
#    def classifyTweet(self, tweet):
#        tweetFeatureMap = {}
#        tweetTime = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
#        for feature in StreamClassifier.extractFeatures(tweet['document']):
#            if feature in self.featureMap: tweetFeatureMap[feature]=self.getFeatureProbabilites(self.featureMap[feature], tweetTime)
#        perClassScores = defaultdict(float)
#        for k, v in tweetFeatureMap.iteritems(): 
#            featureScore = float(StreamClassifier.numberOfClasses)/len(v)
#            if featureScore!=0:
#                for classLabel, score in v.iteritems(): perClassScores[classLabel]+=math.log(featureScore*score)
#        return perClassScores
    
if __name__ == '__main__':
    streamClassifier = StreamClassifierWithDecay(decayRate=Settings.stream_classifier_decay_rate, currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=25)
    streamClassifier.classifyingMethod = streamClassifier.classifyForAUCM
    streamClassifier.start()
    print len(streamClassifier.classifiedDocuments)
    print streamClassifier.getAUCM()

