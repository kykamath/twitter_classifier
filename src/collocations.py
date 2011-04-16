'''
Created on Apr 15, 2011

@author: kykamath
'''
import nltk
from nltk.collocations import BigramCollocationFinder
from settings import Settings
from datasets import DocumentType, DataDirection
from utilities import Utilities
from datetime import timedelta
from collections import defaultdict

maxLength=16
idealModelLength = 8

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
        Utilities.createDirectory(self.collocationsFile)
        finder = BigramCollocationFinder.from_words(Utilities.getWords(fileNameMethod=Utilities.getTrainingFile, dataDirection=DataDirection.past, **self.kwargs))
        finder.apply_word_filter(lambda w: w in Utilities.stopwords)
        scored = finder.score_ngrams(self.getMeasure())
        for ((u,v),s) in scored[:int(len(scored)*Settings.collocations_percentage_of_collocations_to_output)]: Utilities.writeDataToFile(' '.join([u,v,str(s)]), self.collocationsFile)
        
    def load(self):
        self.collocatedTerms = defaultdict(set)
        for line in open(self.collocationsFile):
            u, v = line.strip().split()[:2]
            self.collocatedTerms[u].add(v), self.collocatedTerms[v].add(u) 
            
class GenerateCollocations:
    @staticmethod
    def generate():
        global maxLength, idealModelLength
        currentDay = Settings.startTime
        collocationMeasures = [Collocations.measureTypeRawFrequency, Collocations.measureTypeChiSquare, Collocations.measureTypeLikelihoodRatio, Collocations.measureTypePMI, Collocations.measureTypeStudentT]
        while currentDay<=Settings.endTime:
            noOfDaysList = list(set([idealModelLength]).intersection(set(Utilities.getClassifierLengthsByDay(currentDay, maxLength))))
            for noOfDays in noOfDaysList: 
                for collocationMeasure in collocationMeasures:  
                    print currentDay, collocationMeasure, noOfDays
                    Collocations(collocationMeasure, currentTime=currentDay, numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=noOfDays).discoverAndWrite()
            currentDay+=timedelta(days=1)

if __name__ == '__main__':
    collocation = Collocations(Collocations.measureTypeChiSquare, currentTime=Settings.startTime+timedelta(days=8), numberOfExperts=Settings.numberOfExperts, dataType=DocumentType.typeRuuslUnigram, noOfDays=8)
    collocation.load()
    for k, v in collocation.collocatedTerms.iteritems():
        print k, v