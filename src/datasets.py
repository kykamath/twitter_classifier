'''
Created on Mar 18, 2011

@author: kykamath
'''
import cjson, re
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import timedelta
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

class DataDirection: future = 1; past=-1

class DocumentType(object):
    typeRaw = 'typeRaw' # Original file
    typeRuuslUnigram = 'removed_url_users_specialcharaters_and_lemmatized'
    typeRuuslBigram = 'removed_url_users_specialcharaters_and_lemmatized_bigram'
    
    keys = ['class', 'text', 'created_at', 'id']

    def __init__(self, currentTime, outputDataType, numberOfExperts):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DataType.typeRaw, self.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DataType.typeRaw, self.numberOfExperts, bottom=True)
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
                print data['document']
                exit()
                Utilities.writeAsJsonToFile(data, outputFile)
    def getUnigrams(self, text): 
        pattern = re.compile('[\W_]+')
        def removeHTTP(s): return' '.join(filter(lambda x:x.find('http') == -1, s.lower().split()))
        def lemmatizeWords(terms):
            lmtzr = WordNetLemmatizer()
            return [lmtzr.lemmatize(term) for term in terms]
        def removeUsers(sentance): return ' '.join(filter(lambda term: not term.startswith('@'), sentance.split()))
        sentance = removeHTTP(text.lower())
        sentance = removeUsers(sentance)
        returnWords = [pattern.sub('', word) for word, tag in pos_tag(word_tokenize(sentance))]
        returnWords = filter(lambda w: w!='' and len(w)>2, lemmatizeWords(returnWords))
        return returnWords

class DocumentTypeRuuslUnigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslUnigram, self).__init__(currentTime, DocumentType.typeRuuslUnigram, numberOfExperts)
    def modifyDocument(self, text): return self.getUnigrams(text)
    
class DocumentTypeRuuslBigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslUnigram, self).__init__(currentTime, DocumentType.typeRuuslUnigram, numberOfExperts)
    def modifyDocument(self, text): 
        return self.getUnigrams(text)

class CreateTrainingAndTestSets:
    @staticmethod
    def getTweetsFromExperts(expertsList, file):
        for tweet in Utilities.iterateTweetsFromGzip(file):
            if tweet['user']['id_str'] in expertsList: yield tweet
    @staticmethod
    def rawData():
        currentTime = Settings.startTime
        allExpertsTop, allExpertsBottom = ExpertUsers(number=Settings.numberOfExperts), ExpertUsers(number=Settings.numberOfExperts, type=ExpertUsers.typeBottom)
        allExpertsList={}
        for k, v in allExpertsTop.list.iteritems(): allExpertsList[k]=v
        for k, v in allExpertsBottom.list.iteritems(): allExpertsList[k]=v
        while currentTime <= Settings.endTime:
            for numberOfExperts in [Settings.numberOfExperts]:
                trainingFile = Utilities.getTrainingFile(currentTime, DocumentType.typeRaw, numberOfExperts)
                testFile = Utilities.getTestFile(currentTime, DocumentType.typeRaw, numberOfExperts, bottom=True)
                Utilities.createDirectory(trainingFile), Utilities.createDirectory(testFile)
                print numberOfExperts, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)
                for tweet in CreateTrainingAndTestSets.getTweetsFromExperts(allExpertsList, Settings.twitterUsersTweetsFolder+'%s.gz'%Utilities.getDataFile(currentTime)):
                    tweet['class'] = allExpertsList[tweet['user']['id_str']]['class']
                    if tweet['user']['id_str'] in allExpertsTop.list: Utilities.writeAsJsonToFile(tweet, trainingFile)
                    else: Utilities.writeAsJsonToFile(tweet, testFile)
            currentTime+=timedelta(days=1)
    
    @staticmethod
    def createModifiedData():
        currentTime = Settings.startTime
        while currentTime <= Settings.endTime:
            print currentTime
            DocumentTypeRuuslUnigram(currentTime, Settings.numberOfExperts).convert()
            currentTime+=timedelta(days=1)
            
    @staticmethod
    def createModifiedData1(dataTypes):
        currentTime = Settings.startTime
        while currentTime <= Settings.endTime:
            for dataType in dataTypes: dataType(currentTime, Settings.numberOfExperts).convert()
            currentTime+=timedelta(days=1)
            
if __name__ == '__main__':
#    CreateTrainingAndTestSets.rawData()
    CreateTrainingAndTestSets.createModifiedData1([DocumentTypeRuuslBigram])