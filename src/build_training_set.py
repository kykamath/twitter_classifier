'''
Created on Mar 18, 2011

@author: kykamath
'''
from utilities import ExpertUsers
class CreateDocuments:
    @staticmethod
    def createTrainingSetForDifferentNumberOfUsers(length):
        experts = ExpertUsers(number=length)
        print len(experts.list)
        
if __name__ == '__main__':
    CreateDocuments.createTrainingSetForDifferentNumberOfUsers(100)