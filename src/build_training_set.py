'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import datetime, timedelta
import cjson

class CreateDocuments:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def createTrainingSetForDifferentNumberOfUsers(length):
        experts = ExpertUsers(number=length)
        currentTime = Settings.startTime
        while currentTime <= Settings.endTime:
            print Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)
            currentTime+=timedelta(days=1)
#            for tweet in CreateDocuments.getTweetsFromExperts(experts.list, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)):
#                print cjson.encode(tweet)
        
        
if __name__ == '__main__':
    CreateDocuments.createTrainingSetForDifferentNumberOfUsers(1)