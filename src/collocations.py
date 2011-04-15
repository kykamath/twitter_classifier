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
    measureTypeChiSquare = 'chi_sqare'
    measureTypeLikelihoodRatio = 'likelihood_ratio'
    measureTypePMI = 'pmi'
    measureTypeStudentT = 'student_t'
    
    def __init__(self, measureType, **kwargs):
        self.measureType = measureType
        self.kwargs = kwargs
        self.collocationsFile = Utilities.getCollocationsFile(measureType=self.measureType, **self.kwargs)
    def getMeasure(self):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        return {
                Collocations.measureTypeRawFrequency: bigram_measures.raw_freq,
                Collocations.measureTypeChiSquare: bigram_measures.chi_sq,
                Collocations.measureTypeLikelihoodRatio: bigram_measures.likelihood_ratio,
                Collocations.measureTypePMI: bigram_measures.pmi,
                Collocations.measureTypeStudentT: bigram_measures.student_t
                }[self.measureType]
    
    def discoverAndWrite(self):
#        self.collocationsFile = '/tmp/collocations/file'
        finder = BigramCollocationFinder.from_words(Utilities.getWords(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs), window_size = 5)
        finder.apply_word_filter(lambda w: w in Utilities.stopwords)
        scored = finder.score_ngrams(self.getMeasure())
        for i in scored[:10]: print i

Collocations(Collocations.measureTypeChiSquare, currentTime=Settings.startTime, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=1).discoverAndWrite()
    