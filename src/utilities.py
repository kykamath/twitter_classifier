'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
from settings import Settings
import gzip, cjson, os

class ExpertUsers:
    typeTop = 1
    typeBottom = -1
    def __init__(self, number=1250, type=ExpertUsers.typeTop):
        self.number, self.list, self.type = number, defaultdict(dict), type
        usersData = defaultdict(list)
        for l in open(Settings.usersToCrawl): data = l.strip().split(); usersData[data[0]].append(data[1:])
        for k, v in usersData.iteritems(): 
            if self.type == ExpertUsers.typeTop:
                for user in v[:self.number]: self.list[user[1]] = {'screen_name': user[0], 'class':k}
            else:
                for user in v[-self.number:]: self.list[user[1]] = {'screen_name': user[0], 'class':k}
if __name__ == '__main__':
    print ExpertUsers(number=5, type=1).list
    print ExpertUsers(number=5, type=-1).list
            
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
    def getTrainingFile(currentTime, inputType, numberOfExperts): return Settings.twitterClassifierTrainingSetsFolder+'%s/%s/%s'%(numberOfExperts, inputType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getTestFile(currentTime, inputType, numberOfExperts): return Settings.twitterClassifierTestSetsFolder+'%s/%s/%s'%(numberOfExperts, inputType, Utilities.getDataFile(currentTime))
    @staticmethod
    def getCombinedFile(currentTime, inputType): return Settings.twitterClassifierCombinedSetsFolder+'%s/%s'%(inputType, Utilities.getDataFile(currentTime))
