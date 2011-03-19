'''
Created on Mar 18, 2011

@author: kykamath
'''
from collections import defaultdict
class ExpertUsers:
    def __init__(self, number=None):
        self.number = number
#        if self.number==None:
        self.experts = defaultdict(dict)
        for l in open('/data/twitter/users/crawl/users_to_crawl'):
            data = l.strip().split()
            print data
#                self.experts[data[2]]={'screen_name': data[1], 'class':data[0]}


if __name__ == '__main__':
    ExpertUsers()