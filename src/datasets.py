'''
Created on Mar 18, 2011

@author: kykamath
'''
import cjson, re, urllib2
from utilities import ExpertUsers, Utilities
from settings import Settings
from datetime import timedelta
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

def kgram(k, text): return [' '.join(text[i:i+k]) for i in range(len(text)) if len(text[i:i+k])==k]

class DataDirection: future = 1; past=-1

class DocumentType(object):
    typeRaw = 'raw' # Original file
    typeRuuslUnigram = 'removed_url_users_specialcharaters_and_lemmatized' # removed_url_users_specialcharaters_and_lemmatized
#    typeRuuslUnigram = 'ruusl_unigram' # removed_url_users_specialcharaters_and_lemmatized
    typeRuuslBigram = 'ruusl_bigram'
    typeRuuslTrigram = 'ruusl_trigram'
    typeRuuslSparseBigram = 'ruusl_sparse_bigram'
    typeRuuslUnigramWithMeta = 'ruusl_unigram_with_meta'
    typeRuuslUnigramNouns = 'ruusl_unigram_nouns'
    
    keys = ['class', 'text', 'created_at', 'id']

    def __init__(self, currentTime, outputDataType, numberOfExperts):
        self.currentTime = currentTime
        self.numberOfExperts = numberOfExperts
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DocumentType.typeRaw, self.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DocumentType.typeRaw, self.numberOfExperts, bottom=True)
        self.outputTrainingSetFile = Utilities.getTrainingFile(currentTime, outputDataType, self.numberOfExperts)
        self.outputTestSetFile = Utilities.getTestFile(currentTime, outputDataType, self.numberOfExperts, bottom=True)
        Utilities.createDirectory(self.outputTrainingSetFile), Utilities.createDirectory(self.outputTestSetFile)
    def convert(self):
        for inputFile, outputFile in [(self.inputTrainingSetFile, self.outputTrainingSetFile), (self.inputTestSetFile, self.outputTestSetFile)]:
            for tweet in Utilities.iterateTweetsFromFile(inputFile):
                data = {}
                for k in DocumentType.keys: data[k]=tweet[k]
                data['screen_name'] = tweet['user']['screen_name']; data['user_id'] = tweet['user']['id_str']
                data['document'] = self.modifyDocument(data['text'])
                print data['text']
                print data['document']
                exit()
#                Utilities.writeAsJsonToFile(data, outputFile)
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
    def getUnigramsNouns(self, text):
        pattern = re.compile('[\W_]+')
        def removeHTTP(s): return' '.join(filter(lambda x:x.find('http') == -1, s.lower().split()))
        def isNoun(tag): 
            if tag == 'N' or tag[:2] in ['NN', 'NP', 'NR']: return True
        def lemmatizeWords(terms):
            lmtzr = WordNetLemmatizer()
            return [lmtzr.lemmatize(term) for term in terms]
#                    def isNotUserOrStopList(word):
#                        if word not in stoplist and not word.startswith('@'): return True
        def removeUsers(sentance):
            return ' '.join(filter(lambda term: not term.startswith('@'), sentance.split()))
        sentance = removeHTTP(text.lower())
        sentance = removeUsers(sentance)
        returnWords = [pattern.sub('', word) for word, tag in pos_tag(word_tokenize(sentance)) if isNoun(tag)]
        returnWords = filter(lambda w: w!='' and len(w)>2, lemmatizeWords(returnWords))
        return returnWords

class DocumentTypeRuuslUnigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslUnigram, self).__init__(currentTime, DocumentType.typeRuuslUnigram, numberOfExperts)
    def modifyDocument(self, text): return self.getUnigrams(text)

class DocumentTypeRuuslUnigramNouns(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslUnigramNouns, self).__init__(currentTime, DocumentType.typeRuuslUnigramNouns, numberOfExperts)
    def modifyDocument(self, text): return self.getUnigramsNouns(text)
    
class DocumentTypeRuuslBigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslBigram, self).__init__(currentTime, DocumentType.typeRuuslBigram, numberOfExperts)
    def modifyDocument(self, text): return kgram(2, self.getUnigrams(text))

class DocumentTypeRuuslTrigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslTrigram, self).__init__(currentTime, DocumentType.typeRuuslTrigram, numberOfExperts)
    def modifyDocument(self, text): return kgram(3, self.getUnigrams(text))

class DocumentTypeRuuslSparseBigram(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslSparseBigram, self).__init__(currentTime, DocumentType.typeRuuslSparseBigram, numberOfExperts)
    def modifyDocument(self, text):
        returnData, data = [], self.getUnigrams(text)
        for i in range(len(data)-1):
            for j in range(1, 4):
                if (i+j) < len(data): returnData.append('%s %s'%(data[i], data[i+j]))
        return returnData

class DocumentTypeRuuslUnigramWithMeta(DocumentType):
    def __init__(self, currentTime, numberOfExperts): 
        super(DocumentTypeRuuslUnigramWithMeta, self).__init__(currentTime, DocumentType.typeRuuslUnigramWithMeta, numberOfExperts)
        self.inputTrainingSetFile = Utilities.getTrainingFile(currentTime, DocumentType.typeRuuslUnigram, self.numberOfExperts)
        self.inputTestSetFile = Utilities.getTestFile(currentTime, DocumentType.typeRuuslUnigram, self.numberOfExperts, bottom=True)
#    def modifyDocument(self, text): 
#        return self.getUnigrams(text)+DocumentTypeRuuslUnigramWithMeta.getUrlMeta(text)
    def convert(self):
        for inputFile, outputFile in [(self.inputTrainingSetFile, self.outputTrainingSetFile), (self.inputTestSetFile, self.outputTestSetFile)]:
            for tweet in Utilities.iterateTweetsFromFile(inputFile):
                data = {}
                for k in DocumentType.keys: data[k]=tweet[k]
                data['screen_name'] = tweet['screen_name']; data['user_id'] = tweet['user_id']
                data['document'] = tweet['document']+DocumentTypeRuuslUnigramWithMeta.getUrlMeta(data['text'])
                Utilities.writeAsJsonToFile(data, outputFile)
    @staticmethod
    def getUrlMeta(message):
        try:
            urls = filter(lambda term: term.find('http:') >= 0, message.split())
            if len(urls) > 0:
                result = urllib2.urlopen(urls[0])
                url, meta = result.geturl(), []
                tempMeta = filter(lambda x: x.isalpha() or '-' in x or '_' in x >= 0, url.split('/'))
                for m in tempMeta:
                    if '-' in m: meta+=m.split('-')
                    elif '_' in m: meta+=m.split('_')
                    else: meta.append(m)
                return meta
            else: return []
        except : return []


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
    def createModifiedData(dataTypes):
        currentTime = Settings.startTime
        while currentTime <= Settings.endTime:
            for dataType in dataTypes: 
                print currentTime, dataType
                dataType(currentTime, Settings.numberOfExperts).convert()
            currentTime+=timedelta(days=1)

  
if __name__ == '__main__':
#    CreateTrainingAndTestSets.rawData()
    CreateTrainingAndTestSets.createModifiedData([DocumentTypeRuuslUnigramNouns])
