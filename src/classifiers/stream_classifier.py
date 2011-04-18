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

#featureMap = {}
#notClassified = 'not_classified'
#numberOfClasses = 4

#def learnFromTweet(tweet):
#    global featureMap
#    classLabel = tweet['class']
#    for feature in extractFeatures(tweet['document']):
#        if feature not in featureMap: featureMap[feature] = {'stats': {}, 'class': defaultdict(int)}
#        featureMap[feature]['class'][classLabel]+=1
#def getFeatureProbabilites(feature):
#    mapToReturn = {}
#    totalScore = sum(v for v in feature['class'].itervalues())
#    for classLabel, score in feature['class'].iteritems(): mapToReturn[classLabel] = float(score)/totalScore
#    return mapToReturn
#def classifyTweet(tweet):
#    global featureMap, notClassified, numberOfClasses
##    print tweet
##    print tweet['document']
#    tweetFeatureMap = {}
#    for feature in extractFeatures(tweet['document']):
#        if feature in featureMap: 
##            print feature, featureMap[feature]
#            tweetFeatureMap[feature]=getFeatureProbabilites(featureMap[feature])
#    perClassScores = defaultdict(float)
#    for k, v in tweetFeatureMap.iteritems(): 
#        featureScore = float(numberOfClasses)/len(v)
##        print featureScore, v
#        if featureScore!=0:
#            for classLabel, score in v.iteritems(): perClassScores[classLabel]+=math.log(featureScore*score)
#    sortedScores = sorted(perClassScores.iteritems(), key=itemgetter(1), reverse=True)
#    if sortedScores:
#        classLabel, score = sortedScores[0]
##        print score
##        if score > math.log(Settings.stream_classifier_class_probability_threshold): 
#        return classLabel
#    return notClassified

#def stream_classifier(**kwargs):
#    i=1
#    firstDay = Settings.startTime+timedelta(days=2)
#    for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **kwargs):
#        tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
#        if tweet['tweet_type'] == TweetType.train: learnFromTweet(tweet)
#        else:
#            if firstDay<tweetTimeStamp: 
#                print i, classifyTweet(tweet), tweet['class'], tweet['text']
#                if i==25: exit()
#                i+=1
                
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
    def start(self):
        i=1
        firstDay = Settings.startTime+timedelta(days=self.numberOfInitialBufferDays)
        for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **self.kwargs):
            tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
            if tweet['tweet_type'] == TweetType.train: self.learnFromTweet(tweet)
            else:
                if firstDay<tweetTimeStamp: 
                    self.classifyTweet(tweet)
                    print i, self.classifyingMethod(self.classifyTweet(tweet)), tweet['class'], tweet['text']
                    if i==25: exit()
                    i+=1
    def classify(self, perClassScores):
        sortedScores = sorted(perClassScores.iteritems(), key=itemgetter(1), reverse=True)
        if sortedScores: return sortedScores[0][0]
        return StreamClassifier.notClassified
    def getAUCM(self, perClassScores):
        pass
    @staticmethod
    def getFeatureProbabilites(feature):
        mapToReturn = {}
        totalScore = sum(v for v in feature['class'].itervalues())
        for classLabel, score in feature['class'].iteritems(): mapToReturn[classLabel] = float(score)/totalScore
        return mapToReturn
    @staticmethod
    def extractFeatures(document):
        for feature in document:
            if feature not in Utilities.stopwords: yield feature

class StreamClassifierDefault(StreamClassifier):
    def __init__(self, **kwargs):
        super(StreamClassifierDefault, self).__init__(**kwargs)
    def learnFromTweet(self, tweet):
        classLabel = tweet['class']
        for feature in StreamClassifier.extractFeatures(tweet['document']):
            if feature not in self.featureMap: self.featureMap[feature] = {'stats': {}, 'class': defaultdict(int)}
            self.featureMap[feature]['class'][classLabel]+=1 
    def classifyTweet(self, tweet):
        tweetFeatureMap = {}
        for feature in StreamClassifier.extractFeatures(tweet['document']):
            if feature in self.featureMap: tweetFeatureMap[feature]=StreamClassifier.getFeatureProbabilites(self.featureMap[feature])
        perClassScores = defaultdict(float)
        for k, v in tweetFeatureMap.iteritems(): 
            featureScore = float(StreamClassifier.numberOfClasses)/len(v)
            if featureScore!=0:
                for classLabel, score in v.iteritems(): perClassScores[classLabel]+=math.log(featureScore*score)
        return perClassScores
if __name__ == '__main__':
    StreamClassifierDefault(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=3).start()