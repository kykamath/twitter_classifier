'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities

class CreateDocuments:
    @staticmethod
    def getTweetsFromExperts(expertsList):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def createTrainingSetForDifferentNumberOfUsers(length):
        experts = ExpertUsers(number=length)
        print experts.list
        for tweet in CreateDocuments.getTweetsFromExperts(experts.list):
            print tweet
        
        
if __name__ == '__main__':
    CreateDocuments.createTrainingSetForDifferentNumberOfUsers(1)