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
    def getMeasure(self):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        return {
                Collocations.measureTypeRawFrequency: bigram_measures.raw_freq
                }[self.measureType]
    
    def discoverAndWrite(self):
        finder = BigramCollocationFinder.from_words(iterateWordsFromTweetsFile())
        i = 1
        for w in Utilities.getDocuments(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs):
            print i, w
            i+=1
        exit()
        ###### FILTER IT #####
        scored = finder.score_ngrams(self.getMeasure())
        for i in scored:
            print i

Collocations(Collocations.measureTypeRawFrequency, currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).discoverAndWrite()
    