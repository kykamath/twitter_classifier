'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
class ExpertUsers:
    def __init__(self, number=1250):
        self.number, self.users = number, defaultdict(dict)
        usersData = defaultdict(list)
        for l in open('/data/twitter/users/crawl/users_to_crawl'): data = l.strip().split(); usersData[data[0]].append(data[1:])
        for k, v in usersData.iteritems(): 
            for user in v[:self.number]: self.users[user[1]] = {'screen_name': user[0], 'class':k}
        for k,v in self.users.iteritems(): print k, v
        
#                self.experts[data[2]]={'screen_name': data[1], 'class':data[0]}


if __name__ == '__main__':
    ExpertUsers()