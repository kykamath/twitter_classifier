'''
Created on Apr 15, 2011

@author: kykamath
'''
import nltk
from nltk.collocations import BigramCollocationFinder
from settings import Settings
from datasets import DocumentType
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
        print Utilities.getTrainingFile(**self.kwargs)
        exit()
        ###### FILTER IT #####
        scored = finder.score_ngrams(self.getMeasure())
        for i in scored:
            print i

Collocations(Collocations.measureTypeRawFrequency, currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram).discoverAndWrite()
    