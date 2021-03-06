'''
Created on Apr 18, 2011

@author: kykamath
'''
from collections import defaultdict
from operator import itemgetter
import commands, os, pprint


class GibbsLDA(object):
    def __init__(self, documents, numberOfTopics):
        self.documents = documents
        self.numberOfTopics = numberOfTopics
        self.distribution = None
        self.topWords = defaultdict(list)
        self.clusterIdToClass = {}
    
    def _createDataFile(self, directory):
        os.mkdir(directory)
        fileName = directory +'/%s' % commands.getoutput('dd if=/dev/urandom count=128 bs=1 2>&1 | md5sum | cut -b-20')
        f = open(fileName, 'w')
        f.write('%s\n'%str(len(self.documents)))
        for d in self.documents: f.write('%s\n'%d)
        f.close()
        return fileName
    
    def _getDocumentDistribution(self, directory):
        self.distribution, i = {}, 0
        for line in map(lambda l: l.strip().split(), open(directory+'/model-final.theta')):
            dist = [float(l) for l in line]
            self.distribution[i] = dist.index(sorted(dist, reverse = True)[0])
            i+=1
    
#    def _getTopWords(self, directory):
#        currentTopic = None
#        for line in map(lambda l: l.strip().split(), open(directory+'/model-final.twords')):
#            if line[0] == 'Topic': currentTopic = line[1][:-3]
#            else: self.topWords[currentTopic].append(line[0])
    
    def getDistributionAcrossTopics(self):
        directory = '/tmp/' + commands.getoutput('dd if=/dev/urandom count=128 bs=1 2>&1 | md5sum | cut -b-20')
        fileName = self._createDataFile(directory)
        os.system('lda -est -alpha 0.1 -beta 0.1 -ntopics %s -niters 1000 -twords 20 -savestep 2001 -dfile %s' % (str(self.numberOfTopics), fileName))
        self._getDocumentDistribution(directory)
#        self._getTopWords(directory)
        os.system('rm -rf %s' % directory)
        return self.distribution
        
class ReLabelTrainingDocuments:
    numberOfTopics = 4
    def __init__(self, documents): self.originalDocuments = [(' '.join(d[0]), d[1]) for d in documents if d[0]]
    def getRelabeledDocuments(self):
        def getClusterLabelsToOriginalLabelsMap(clusteredDocuments, clusterLabelsToOriginalLabelMap):
            clusterLabelsToOriginalLabelsDistribution = {}
            for ((document, originalLabel), clusterLabel) in zip(self.originalDocuments, clusteredDocuments.values()):
                if clusterLabel not in clusterLabelsToOriginalLabelsDistribution: clusterLabelsToOriginalLabelsDistribution[clusterLabel] = defaultdict(int)
                clusterLabelsToOriginalLabelsDistribution[clusterLabel][originalLabel]+=1
            for clusterLabel, distribution in clusterLabelsToOriginalLabelsDistribution.iteritems():
                clusterLabelsToOriginalLabelMap[clusterLabel] = sorted(distribution.iteritems(), key=itemgetter(1), reverse=True)[0][0]
        clusterLabelsToOriginalLabelMap = {}
        clusteredDocuments = GibbsLDA([d[0] for d in self.originalDocuments], ReLabelTrainingDocuments.numberOfTopics).getDistributionAcrossTopics()
        getClusterLabelsToOriginalLabelsMap(clusteredDocuments, clusterLabelsToOriginalLabelMap)
        for ((document, originalLabel), clusterLabel) in zip(self.originalDocuments, clusteredDocuments.values()): yield (document.split(), clusterLabelsToOriginalLabelMap[clusterLabel])

if __name__ == '__main__':
    documents = [("Human machine interface for lab abc computer applications".split(), 'politics'),
                 ("Human machine interface for lab abc computer applications".split(), 'politics'),
                 ("Human machine interface for lab abc computer applications".split(), 'politics'),
                      ("A survey of user opinion of computer system response time".split(), 'politics'),
                      ("The EPS user interface management system".split(), 'sports'),
                      ("System and human system engineering testing of EPS".split(), 'entertainment'),
                      ("Relation of user perceived response time to error measurement".split(), 'technology'),
                       ("Graph minors A survey".split(), 'technology')]
    pprint.pprint(list(ReLabelTrainingDocuments(documents).getRelabeledDocuments()))