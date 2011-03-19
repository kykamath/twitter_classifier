'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities
from settings import Settings
import cjson

class CreateDocuments:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def createTrainingSetForDifferentNumberOfUsers(length):
        experts = ExpertUsers(number=length)
        print experts.list
        for tweet in CreateDocuments.getTweetsFromExperts(experts.list, Settings.twitterUsersTweetsFolder+'2011_3_10.gz'):
            print cjson.encode(tweet)
        
        
if __name__ == '__main__':
    CreateDocuments.createTrainingSetForDifferentNumberOfUsers(1)