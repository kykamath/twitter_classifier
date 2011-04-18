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

def stream_classifier(**kwargs):
    firstDay = Settings.startTime+timedelta(days=1)
    for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.future, completeTweets=True, **kwargs):
        tweetTimeStamp = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
        if tweet['tweet_type'] == TweetType.train: print 'learn'
        else:
            if firstDay<tweetTimeStamp: print 'test'
if __name__ == '__main__':
    stream_classifier(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=10)