'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import datetime, timedelta
import cjson

class CreateTrainingAndTestSets:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def byNumberOfExpertUsers():
        currentTime = Settings.startTime
        allExperts = experts = ExpertUsers()
        while currentTime <= Settings.endTime:
            for numberOfExperts in Settings.expertListSizes:
                expertsForTraining = ExpertUsers(number=numberOfExperts)
                trainingFile = Settings.twitterClassifierTrainingSetsFolder+'%s/%s'%(numberOfExperts,Utilities.getDataFile(currentTime))
                testFile = Settings.twitterClassifierTestSetsFolder+'%s/%s'%(numberOfExperts,Utilities.getDataFile(currentTime))
                Utilities.createDirectory(trainingFile), Utilities.createDirectory(testFile)
                for tweet in CreateTrainingAndTestSets.getTweetsFromExperts(allExperts.list, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)):
                    tweet['class'] = allExperts.list[tweet['user']['id_str']]['class']
                    if tweet['user']['id_str'] in expertsForTraining.list: Utilities.writeAsJsonToFile(tweet, trainingFile)
                    else: Utilities.writeAsJsonToFile(tweet, testFile)
            currentTime+=timedelta(days=1)
    
    @staticmethod
    def combineExpertUsers():
        currentTime, numberOfExperts = Settings.startTime, 50
        while currentTime <= Settings.endTime:
            trainingFile = Settings.twitterClassifierTrainingSetsFolder+'%s/%s'%(numberOfExperts,Utilities.getDataFile(currentTime))
            testFile = Settings.twitterClassifierTestSetsFolder+'%s/%s'%(numberOfExperts,Utilities.getDataFile(currentTime))
            combinedFile = Settings.twitterClassifierAllFolder+'%s'%(Utilities.getDataFile(currentTime))
            print combinedFile
            Utilities.createDirectory(combinedFile)
            for tweet in open(trainingFile):
                tweet = cjson.decode(tweet)
                Utilities.writeAsJsonToFile(tweet, combinedFile)
            for tweet in open(testFile):
                tweet = cjson.decode(tweet)
                Utilities.writeAsJsonToFile(tweet, combinedFile)
            currentTime+=timedelta(days=1)
        
if __name__ == '__main__':
    CreateTrainingAndTestSets.combineExpertUsers()