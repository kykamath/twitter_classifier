'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import datetime, timedelta
import cjson, pprint, re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

numberOfExperts = 125

class DataType(object):
    raw = 'raw' # Original file
    raw_unigram = 'removed_url_users_specialcharaters_and_lemmatized'
    
    keys = ['class', 'text', 'created_at', 'id']

    def __init__(self, currentTime, outputDataType, numberOfExperts):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DataType.raw, self.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DataType.raw, self.numberOfExperts, bottom=True)
        self.outputTrainingSetFile = Utilities.getTrainingFile(currentTime, outputDataType, self.numberOfExperts)
        self.outputTestSetFile = Utilities.getTestFile(currentTime, outputDataType, self.numberOfExperts, bottom=True)
        Utilities.createDirectory(self.outputTrainingSetFile), Utilities.createDirectory(self.outputTestSetFile)
    def convert(self):
        for inputFile, outputFile in [(self.inputTrainingSetFile, self.outputTrainingSetFile), (self.inputTestSetFile, self.outputTestSetFile)]:
            for tweet in Utilities.iterateTweetsFromFile(inputFile):
                data = {}
                for k in DataType.keys: data[k]=tweet[k]
                data['screen_name'] = tweet['user']['screen_name']; data['user_id'] = tweet['user']['id_str']
                data['document'] = self.modifyDocument(data['text'])
#                Utilities.writeAsJsonToFile(data, outputFile)
                pprint.pprint(data)
                exit()

class DocumentTypeRawUnigram(DataType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRawUnigram, self).__init__(currentTime, DataType.raw_unigram, numberOfExperts)
    def modifyDocument(self, text): 
        pattern = re.compile('[\W_]+')
        def removeHTTP(s): return' '.join(filter(lambda x:x.find('http') == -1, s.lower().split()))
        def lemmatizeWords(terms):
            lmtzr = WordNetLemmatizer()
            return [lmtzr.lemmatize(term) for term in terms]
        def removeUsers(sentance): return ' '.join(filter(lambda term: not term.startswith('@'), sentance.split()))
        sentance = removeHTTP(text.lower())
        sentance = removeUsers(sentance)
        returnWords = [pattern.sub('', word) for word, tag in pos_tag(word_tokenize(sentance))]
        returnWords = filter(lambda w: w!='', lemmatizeWords(returnWords))
        return returnWords

class CreateTrainingAndTestSets:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def rawData():
        global numberOfExperts
        currentTime = Settings.startTime
        allExpertsTop, allExpertsBottom = ExpertUsers(number=numberOfExperts), ExpertUsers(number=numberOfExperts, type=ExpertUsers.typeBottom)
        allExpertsList={}
        for k, v in allExpertsTop.list.iteritems(): allExpertsList[k]=v
        for k, v in allExpertsBottom.list.iteritems(): allExpertsList[k]=v
        while currentTime <= Settings.endTime:
            for numberOfExperts in [numberOfExperts]:
                trainingFile = Utilities.getTrainingFile(currentTime, DataType.raw, numberOfExperts)
                testFile = Utilities.getTestFile(currentTime, DataType.raw, numberOfExperts, bottom=True)
                Utilities.createDirectory(trainingFile), Utilities.createDirectory(testFile)
                print numberOfExperts, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)
                for tweet in CreateTrainingAndTestSets.getTweetsFromExperts(allExpertsList, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)):
                    tweet['class'] = allExpertsList[tweet['user']['id_str']]['class']
                    if tweet['user']['id_str'] in allExpertsTop.list: Utilities.writeAsJsonToFile(tweet, trainingFile)
                    else: Utilities.writeAsJsonToFile(tweet, testFile)
            currentTime+=timedelta(days=1)
    
    @staticmethod
    def createModifiedData():
        global numberOfExperts
        currentTime = Settings.startTime
        while currentTime <= Settings.endTime:
            DocumentTypeRawUnigram(currentTime, numberOfExperts).convert()
            currentTime+=timedelta(days=1)
            
#    @staticmethod
#    def combineRawData():
#        currentTime, numberOfExperts = Settings.startTime, numberOfExperts
#        while currentTime <= Settings.endTime:
#            trainingFile = Utilities.getTrainingFile(currentTime, DataType.raw, numberOfExperts)
#            testFile = Utilities.getTestFile(currentTime, DataType.raw, numberOfExperts)
#            combinedFile = Utilities.getCombinedFile(currentTime, DataType.raw)
#            print trainingFile, testFile, combinedFile
#            Utilities.createDirectory(combinedFile)
#            for tweet in open(trainingFile):
#                tweet = cjson.decode(tweet)
#                Utilities.writeAsJsonToFile(tweet, combinedFile)
#            for tweet in open(testFile):
#                tweet = cjson.decode(tweet)
#                Utilities.writeAsJsonToFile(tweet, combinedFile)
#            currentTime+=timedelta(days=1)
    
#    @staticmethod
#    def splitFileByHours():
#        file = Settings.twitterClassifierAllFolder+'%s'%(Utilities.getDataFile(datetime(2011,3,11)))
#        for tweet in Utilities.iterateTweetsFromFile(file):
#            outputFile = Settings.twitterDataFolder+'classifier/%s/%s'%(Utilities.getDataFile(datetime(2011,3,11)), 
#                                                                        datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format).hour)
#            Utilities.createDirectory(outputFile)
#            Utilities.writeAsJsonToFile(tweet, outputFile)

if __name__ == '__main__':
#    DocumentTypeRawUnigram(Settings.startTime).convert()
    CreateTrainingAndTestSets.createModifiedData()