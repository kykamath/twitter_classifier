'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
from settings import Settings
class ExpertUsers:
    def __init__(self, number=1250):
        self.number, self.list = number, defaultdict(dict)
        usersData = defaultdict(list)
        for l in open(Settings.usersToCrawl): data = l.strip().split(); usersData[data[0]].append(data[1:])
        for k, v in usersData.iteritems(): 
            for user in v[:self.number]: self.list[user[1]] = {'screen_name': user[0], 'class':k}

