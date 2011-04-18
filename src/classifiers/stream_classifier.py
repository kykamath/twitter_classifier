'''
Created on Apr 17, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
from datasets import DataDirection, DocumentType
from utilities import Utilities
from settings import Settings
from datetime import datetime, timedelta

def stream_classifier(**kwargs):
    for tweet in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.past, completeTweets=True, **kwargs):
        print datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format).day
    
if __name__ == '__main__':
    stream_classifier(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=1)