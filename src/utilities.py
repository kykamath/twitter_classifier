'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
from settings import Settings
import gzip, cjson, os
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
    def getDataFile(currentTime): return '_'.join([str(currentTime.year), str(currentTime.month), str(currentTime.day)])
    @staticmethod
    def createDirectory(path):
        dir = path[:path.rfind('/')]
        if not os.path.exists(dir): os.umask(0), os.makedirs('%s'%dir, 0770)
    @staticmethod
    def writeAsJsonToFile(data, file):
        f = open(file, 'a')
        f.write(cjson.encode(data)+'\n')
        f.close()
    @staticmethod
    def getTrainingFile(currentTime, dataType, numberOfExperts, **kwargs): 
        return Settings.twitterClassifierTrainingSetsFolder+'%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTestFile(currentTime, dataType, numberOfExperts, bottom=False, **kwargs): 
        if not bottom: return Settings.twitterClassifierTestSetsFolder+'%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
        else: return Settings.twitterClassifierTestSetsFolder+'_%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTrainedClassifierFile(currentTime, dataType, numberOfExperts, historyLength, **kwargs):
        return Settings.twitterClassifierTrainedModelsFolder +'%s/%s/%s/%s'%(numberOfExperts, dataType, Utilities.getDataFile(currentTime), historyLength)
    @staticmethod
    def getDocuments(**kwargs):
        currentTime=kwargs['currentTime']
        fileNameMethod=kwargs['fileNameMethod']
        for i in range(kwargs['historyLength']):
            fileName = fileNameMethod(**kwargs)
            for tweet in Utilities.iterateTweetsFromFile(fileName): yield (tweet['document'], tweet['class'])
            currentTime-=timedelta(days=1)
#    @staticmethod
#    def getCombinedFile(currentTime, dataType): return Settings.twitterClassifierCombinedSetsFolder+'%s/%s'%(dataType, Utilities.getDataFile(currentTime))
