'''
Created on Apr 17, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
from datasets import DataDirection, DocumentType, TweetType
from utilities import Utilities
from settings import Settings
from datetime import datetime, timedelta
from collections import defaultdict

featureMap = {}

def learnFromTweet(tweet):
    global featureMap
    classLabel = tweet['class']
    for feature in tweet['document']:
        if feature not in featureMap: featureMap[feature] = {'stats': {}, 'class': defaultdict(int)}
        featureMap[feature]['class'][classLabel]+=1
def classifyTweet(tweet):
    global featureMap
    print tweet
    flag = False
    for feature in tweet['document']:
        if feature in featureMap: 
            flag=True
            print feature, featureMap[feature]
    if flag: exit()

def stream_classifier(**kwargs):
    firstDay = Settings.startTime+timedelta(days=1)
    for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **kwargs):
        tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
        if tweet['tweet_type'] == TweetType.train: learnFromTweet(tweet)
        else:
            if firstDay<tweetTimeStamp: classifyTweet(tweet)
if __name__ == '__main__':
    stream_classifier(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=1)