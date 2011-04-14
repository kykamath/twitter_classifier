'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import datetime, timedelta
import cjson, pprint

class DataType(object):
    raw = 'raw' # Original file
    raw_unigram = 'raw_unigram' # Original file with unigrams
    
    keys = ['class', 'text', 'created_at', 'id']
    numberOfExperts = 250

    def __init__(self, currentTime, outputDataType):
        self.currentTime = currentTime
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DataType.raw, DataType.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DataType.raw, DataType.numberOfExperts)
        self.outputTrainingSetFile = Utilities.getTrainingFile(currentTime, outputDataType, DataType.numberOfExperts)
        self.outputTestSetFile = Utilities.getTestFile(currentTime, outputDataType, DataType.numberOfExperts)
        Utilities.createDirectory(self.outputTrainingSetFile), Utilities.createDirectory(self.outputTestSetFile)
    def convert(self):
        for inputFile, outputFile in [(self.inputTrainingSetFile, self.outputTrainingSetFile), (self.inputTestSetFile, self.outputTestSetFile)]:
            for tweet in Utilities.iterateTweetsFromFile(inputFile):
                data = {}
                for k in DataType.keys: data[k]=tweet[k]
                data['screen_name'] = tweet['user']['screen_name']; data['user_id'] = tweet['user']['id_str']
                data['document'] = self.modifyDocument(data['text'])
                Utilities.writeAsJsonToFile(data, outputFile)
                exit()

class DocumentTypeRawUnigram(DataType):
    def __init__(self, currentTime): super(DocumentTypeRawUnigram, self).__init__(currentTime, DataType.raw_unigram)
    def modifyDocument(self, text): return text.strip().lower().split()

class CreateTrainingAndTestSets:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def rawData():
        currentTime = Settings.startTime
        allExperts = ExpertUsers()
        while currentTime <= Settings.endTime:
#            for numberOfExperts in Settings.expertListSizes:
            for numberOfExperts in [250]:
                expertsForTraining = ExpertUsers(number=numberOfExperts)
                trainingFile = Utilities.getTrainingFile(currentTime, DataType.raw, numberOfExperts)
                testFile = Utilities.getTestFile(currentTime, DataType.raw, numberOfExperts)
                Utilities.createDirectory(trainingFile), Utilities.createDirectory(testFile)
                print numberOfExperts, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)
                for tweet in CreateTrainingAndTestSets.getTweetsFromExperts(allExperts.list, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)):
                    tweet['class'] = allExperts.list[tweet['user']['id_str']]['class']
                    if tweet['user']['id_str'] in expertsForTraining.list: Utilities.writeAsJsonToFile(tweet, trainingFile)
                    else: Utilities.writeAsJsonToFile(tweet, testFile)
            currentTime+=timedelta(days=1)
    
    @staticmethod
    def combineRawData():
        currentTime, numberOfExperts = Settings.startTime, 250
        while currentTime <= Settings.endTime:
            trainingFile = Utilities.getTrainingFile(currentTime, DataType.raw, numberOfExperts)
            testFile = Utilities.getTestFile(currentTime, DataType.raw, numberOfExperts)
            combinedFile = Utilities.getCombinedFile(currentTime, DataType.raw)
            print trainingFile, testFile, combinedFile
            Utilities.createDirectory(combinedFile)
            for tweet in open(trainingFile):
                tweet = cjson.decode(tweet)
                Utilities.writeAsJsonToFile(tweet, combinedFile)
            for tweet in open(testFile):
                tweet = cjson.decode(tweet)
                Utilities.writeAsJsonToFile(tweet, combinedFile)
            currentTime+=timedelta(days=1)
    
#    @staticmethod
#    def splitFileByHours():
#        file = Settings.twitterClassifierAllFolder+'%s'%(Utilities.getDataFile(datetime(2011,3,11)))
#        for tweet in Utilities.iterateTweetsFromFile(file):
#            outputFile = Settings.twitterDataFolder+'classifier/%s/%s'%(Utilities.getDataFile(datetime(2011,3,11)), 
#                                                                        datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format).hour)
#            Utilities.createDirectory(outputFile)
#            Utilities.writeAsJsonToFile(tweet, outputFile)

if __name__ == '__main__':
    DocumentTypeRawUnigram(Settings.startTime).convert()