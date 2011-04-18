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

featureMap = {}
notClassified = 'not_classified'

def extractFeatures(document):
    for feature in document:
        if feature not in Utilities.stopwords: yield feature

def learnFromTweet(tweet):
    global featureMap
    classLabel = tweet['class']
    for feature in extractFeatures(tweet['document']):
        if feature not in featureMap: featureMap[feature] = {'stats': {}, 'class': defaultdict(int)}
        featureMap[feature]['class'][classLabel]+=1
def getFeatureProbabilites(feature):
    mapToReturn = {}
    totalScore = sum(v for v in feature['class'].itervalues())
    for classLabel, score in feature['class'].iteritems(): mapToReturn[classLabel] = float(score)/totalScore
    return mapToReturn
def classifyTweet(tweet):
    global featureMap, notClassified
    tweetFeatureMap = {}
    for feature in extractFeatures(tweet['document']):
        if feature in featureMap: tweetFeatureMap[feature]=getFeatureProbabilites(featureMap[feature])
    perClassScores = defaultdict(float)
    for k, v in tweetFeatureMap.iteritems(): 
        for classLabel, score in v.iteritems(): perClassScores[classLabel]+=math.log(score)
    sortedScores = sorted(perClassScores.iteritems(), key=itemgetter(1), reverse=True)
    if sortedScores:
        classLabel, score = sortedScores[0]
        print score
#        if score > math.log(Settings.stream_classifier_class_probability_threshold): 
        return classLabel
    return notClassified

def stream_classifier(**kwargs):
    i=1
    firstDay = Settings.startTime+timedelta(days=2)
    for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **kwargs):
        tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
        if tweet['tweet_type'] == TweetType.train: learnFromTweet(tweet)
        else:
            if firstDay<tweetTimeStamp: 
                print i, classifyTweet(tweet), tweet['class'], tweet['text']
                if i==25: exit()
                i+=1
if __name__ == '__main__':
    stream_classifier(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=1)