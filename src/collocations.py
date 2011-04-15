'''
Created on Apr 15, 2011

@author: kykamath
'''
import nltk
from nltk.collocations import BigramCollocationFinder
from settings import Settings
from datasets import DocumentType, DataDirection
from utilities import Utilities

def iterateWordsFromTweetsFile():
    for i in ['sd', 'asd', 'asds', 'asd', 'asds', 'asd']: yield i

class Collocations:
    measureTypeRawFrequency = 'frequency'
    
    def __init__(self, measureType, **kwargs):
        self.measureType = measureType
        self.kwargs = kwargs
        self.collocationsFile = Utilities.getCollocationsFile(measureType=self.measureType, **self.kwargs)
    def getMeasure(self):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        return {
                Collocations.measureTypeRawFrequency: bigram_measures.raw_freq
                }[self.measureType]
    
    def discoverAndWrite(self):
        i = 1
        for w in Utilities.getWords(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs):
            print i, w
            i+=1
        print self.collocationsFile
        exit()
#        self.collocationsFile = '/tmp/collocations/file'
        finder = BigramCollocationFinder.from_words(iterateWordsFromTweetsFile())
        ###### FILTER IT #####
        
        scored = finder.score_ngrams(self.getMeasure())
        for i in scored:         print i

Collocations(Collocations.measureTypeRawFrequency, currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).discoverAndWrite()
    