'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
from settings import Settings
import gzip, cjson, os, math
from datetime import timedelta

class ExpertUsers:
    typeTop = 1
    typeBottom = -1
    def __init__(self, number=1250, type=typeTop):
        self.number, self.list, self.type = number, defaultdict(dict), type
        usersData = defaultdict(list)
        for l in open(Settings.usersToCrawl): data = l.strip().split(); usersData[data[0]].append(data[1:])
        for k, v in usersData.iteritems(): 
            if self.type == ExpertUsers.typeTop:
                for user in v[:self.number]: self.list[user[1]] = {'screen_name': user[0], 'class':k}
            else:
                for user in v[-self.number:]: self.list[user[1]] = {'screen_name': user[0], 'class':k}
            
class Utilities:
    stopwords = [l.strip() for l in open(Settings.applicationCommonFilesFolder+'stopwords')]
    
    @staticmethod
    def my_log(val):
        if val==0: return 0.0
        else: return math.log(val)
    
    @staticmethod
    def iterateTweetsFromGzip(file):
        for line in gzip.open(file, 'rb'): 
            try:
                data = cjson.decode(line)
                if 'text' in data: yield data
            except: pass
    @staticmethod
    def iterateTweetsFromFile(file):
        for line in open(file): 
            try:
                data = cjson.decode(line)
                if 'text' in data: yield data
            except: pass
    @staticmethod
    def iterateTweetsFromFileWithTerminatingNone(file):
        for line in Utilities.iterateTweetsFromFile(file): yield line
        yield None
    @staticmethod
    def iterateJsonFromFile(file):
        for line in open(file): 
            try:
                yield cjson.decode(line)
            except: pass
#    @staticmethod
#    def iterateWordsFromTrainingFile(file):
#        for tweet in Utilities.iterateTweetsFromFile(file):
#            for word in tweet['document']: yield word
            
    @staticmethod        
    def getDataFile(currentTime): return '_'.join([str(currentTime.year), str(currentTime.month), str(currentTime.day)])
    @staticmethod
    def createDirectory(path):
        dir = path[:path.rfind('/')]
        if not os.path.exists(dir): os.umask(0), os.makedirs('%s'%dir, 0777)
    @staticmethod
    def writeAsJsonToFile(data, file):
        f = open(file, 'a')
        f.write(cjson.encode(data)+'\n')
        f.close()
    @staticmethod
    def writeDataToFile(data, file):
        f = open(file, 'a')
        f.write(data+'\n')
        f.close()
    @staticmethod
    def getTrainingFile(currentTime, dataType, numberOfExperts, **kwargs): 
        return Settings.twitterClassifierTrainingSetsFolder+'%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTestFile(currentTime, dataType, numberOfExperts, bottom=False, **kwargs): 
        if not bottom: return Settings.twitterClassifierTestSetsFolder+'%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
        else: return Settings.twitterClassifierTestSetsFolder+'_%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTrainedClassifierFile(classifierType, currentTime, dataType, numberOfExperts, noOfDays, **kwargs):
        return Settings.twitterClassifierTrainedModelsFolder +'%s/%s/%s/%s/%s'%(classifierType, numberOfExperts, dataType, Utilities.getDataFile(currentTime), noOfDays)
    @staticmethod
    def getCollocationsFile(measureType, currentTime, dataType, numberOfExperts, noOfDays, **kwargs):
        return Settings.twitterClassifierCollocationsFolder +'%s/%s/%s/%s/%s'%(measureType, numberOfExperts, dataType, Utilities.getDataFile(currentTime), noOfDays)
    @staticmethod
    def getStreamingSetsFile(currentTime, dataType, numberOfExperts, **kwargs): 
        return Settings.twitterClassifierStreamingSetsFolder+'%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTweets(**kwargs):
        currentTime=kwargs['currentTime']
        fileNameMethod=kwargs['fileNameMethod']
        del kwargs['currentTime']
        completeTweets = False
        if 'completeTweets' in kwargs: completeTweets = True
        for i in range(kwargs['noOfDays']):
            if not completeTweets:
                for tweet in Utilities.iterateTweetsFromFile(fileNameMethod(currentTime=currentTime, **kwargs)): yield (tweet['document'], tweet['class'])
            else:
                for tweet in Utilities.iterateTweetsFromFile(fileNameMethod(currentTime=currentTime, **kwargs)): yield tweet
            currentTime=currentTime+kwargs['dataDirection']*timedelta(days=1)
    @staticmethod
    def getWordsFromTweets(**kwargs):
        for document in Utilities.getTweets(**kwargs):
            for word in document[0]: yield word
    @staticmethod
    def getTweetsWithCollocations(collocations, **kwargs):
        for tweet in Utilities.getTweets(**kwargs):
            terms = set(tweet[0])
            for term in tweet[0]: 
                if term in collocations.collocatedTerms: terms = terms.union(collocations.collocatedTerms[term])
#            if len(terms)!= len(set(tweet[0])): print len(terms), len(tweet[0]), sorted(list(terms)), sorted(set(tweet[0]))
            yield (list(terms), tweet[1])
    @staticmethod
    def getClassifierLengthsByDay(currentDay, maxLength): return [1]+range(2,min([maxLength, (currentDay-Settings.startTime).days+2]),2)
    @staticmethod
    def getTopicForIndex(index):
        if index == '1': return "buisness"
        elif index == '2' : return "entertainment"
        elif index == '3' : return "health"
        elif index == '4' : return "politics"
        elif index == '5' : return "sports"
        elif index == '6' : return "technology"
        elif index == '7' : return "weather"
        elif index == '8' : return "NotClassified"
        elif index == '-1': return "Other"

if __name__ == '__main__':
    print Utilities.my_log(0), Utilities.my_log(1), Utilities.my_log(2)