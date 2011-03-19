'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
class ExpertUsers:
    def __init__(self, number=None):
        self.number = number
        usersData = defaultdict(list)
        for l in open('/data/twitter/users/crawl/users_to_crawl'):
            data = l.strip().split()
            usersData[data[0]].append(data[1:])
        for k, v in usersData.iteritems(): print k, len(v)
            
#                self.experts[data[2]]={'screen_name': data[1], 'class':data[0]}


if __name__ == '__main__':
    ExpertUsers()