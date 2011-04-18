'''
Created on Apr 17, 2011

@author: kykamath
'''
import sys
from datasets import DataDirection, DocumentType
from utilities import Utilities
from settings import Settings
sys.path.append('../')
def stream_classifier(**kwargs):
    for t in Utilities.getTweets(fileNameMethod=Utilities.getStreamingSetsFile, dataDirection=DataDirection.past, **kwargs):
        print t
    
if __name__ == '__main__':
    stream_classifier(currentTime=Settings.startTime, dataType=DocumentType.typeRuuslUnigram, numberOfExperts=Settings.numberOfExperts, noOfDays=1)