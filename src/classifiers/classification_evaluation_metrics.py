'''
Created on Mar 27, 2011

@author: kykamath
'''
import numpy
from numpy import *
from scipy import *
from scipy.stats import mode
from scipy.misc.common import factorial
from operator import itemgetter
from collections import defaultdict

def combination(a,k):
    result=1
    for i in range(k):
        result=result*((a-i)/(k-i))
    return result
 
def P(predicted,labels):
    K=unique(predicted)
    p=0
    for cls in K:
        cls_members=nonzero(predicted==cls)[0]
        if cls_members.shape[0]<=1:
            continue
        real_label=mode(labels[cls_members])[0][0]
        correctCount=nonzero(labels[cls_members]==real_label)[0].shape[0]
        p+=double(correctCount)/cls_members.shape[0]
    return p/K.shape[0]
 
 
def R(predicted,labels):
    K=unique(predicted)
    ccount=0
    for cls in K:
        cls_members=nonzero(predicted==cls)[0]
        real_label=mode(labels[cls_members])[0][0]
        ccount+=nonzero(labels[cls_members]==real_label)[0].shape[0]
    return double(ccount)/predicted.shape[0]

class ClassificationEvaluationMetrics:
    
    metricF = 'f'
    metricPurity = 'purity'
    
    @staticmethod
    def use(predicted, metric):
        if metric==ClassificationEvaluationMetrics.metricF: return ClassificationEvaluationMetrics.getValue(predicted, ClassificationEvaluationMetrics.F)
        elif metric==ClassificationEvaluationMetrics.metricPurity: return ClassificationEvaluationMetrics.getValue(predicted, ClassificationEvaluationMetrics.purity)
        else: raise Exception('Not registered metric.')
     
    @staticmethod
    def F(predicted,labels):
        p=P(predicted,labels)
        r=R(predicted,labels)
        return 2*p*r/(p+r),p,r
     
    #Adjusted purity
    #http://acl.ldc.upenn.edu/acl2002/MAIN/pdfs/Main303.pdf
    @staticmethod
    def APP(predicted,labels):
        K=unique(predicted)
        app=0.0
        for cls in K:
            cls_members=nonzero(predicted==cls)[0]
            if cls_members.shape[0]<=1:
                continue
            real_labels=labels[cls_members]
            correct_pairs=0
            for i in range(real_labels.shape[0]):
                for i2 in range(i+1):
                    if real_labels[i]==real_labels[i2]:
                            correct_pairs+=2
            total=cls_members.shape[0]
            total_pairs=total+1
            app+=double(correct_pairs)/(total_pairs*total)
        return double(app)/K.shape[0]
    
    # Purity 
    @staticmethod
    def purity(predicted,labels):
        correctAssignedItems = 0.0
        for u,v in zip(predicted,labels):
            if u==v: correctAssignedItems+=1
        return correctAssignedItems/len(predicted) 
     
    #Mutual information
    @staticmethod
    def mutual_info(x,y):
        N=double(x.size)
        I=0.0
        eps = numpy.finfo(float).eps
        for l1 in unique(x):
            for l2 in unique(y):
                #Find the intersections
                l1_ids=nonzero(x==l1)[0]
                l2_ids=nonzero(y==l2)[0]
                pxy=(double(intersect1d(l1_ids,l2_ids).size)/N)+eps
                I+=pxy*log2(pxy/((l1_ids.size/N)*(l2_ids.size/N)))
        return I
     
         
    #Normalized mutual information
    @staticmethod
    def nmi(x,y):
        N=x.size
        I=ClassificationEvaluationMetrics.mutual_info(x,y)
        Hx=0
        for l1 in unique(x):
            l1_count=nonzero(x==l1)[0].size
            Hx+=-(double(l1_count)/N)*log2(double(l1_count)/N)
        Hy=0
        for l2 in unique(y):
            l2_count=nonzero(y==l2)[0].size
            Hy+=-(double(l2_count)/N)*log2(double(l2_count)/N)
        return I/((Hx+Hy)/2)
    @staticmethod
    def grp2idx(labels):
        inds=dict()
        for label in labels:
            if label not in inds:
                inds[label]=len(inds)
        return array([inds[label] for label in labels])
     
    #Vmeasure
    @staticmethod
    def V(predicted,labels):
        predicted=ClassificationEvaluationMetrics.grp2idx(predicted)
        labels=ClassificationEvaluationMetrics.grp2idx(labels)
         
        a=zeros((unique(labels).size,unique(predicted).size))
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]):
                a[i,i2]=intersect1d(nonzero(labels==i)[0],nonzero(predicted==i2)[0]).size
        N=labels.size
        n=a.shape[0]
        a=double(a)
        Hck=0
        Hc=0
        Hkc=0
        Hk=0
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]):
                if a[i,i2]>0:
                    Hkc+=(a[i,i2]/N)*log(a[i,i2]/sum(a[i,:]))
                    Hck+=(a[i,i2]/N)*log(a[i,i2]/sum(a[:,i2]))
            Hc+=(sum(a[i,:])/N)*log(sum(a[i,:])/N)
        Hck=-Hck
        Hkc=-Hkc
        Hc=-Hc
        for i in range(a.shape[1]):
            ak=sum(a[:,i])
            Hk+=(ak/n)*log(ak/N)
        Hk=-Hk
         
        h=1-(Hck/Hc)
        c=1-(Hkc/Hc)
        vmeasure=(2*h*c)/(h+c)
        return vmeasure
     
    #Mutal information
    #http://acl.ldc.upenn.edu/acl2002/MAIN/pdfs/Main303.pdf
    @staticmethod
    def mi(predicted,labels):
        predicted=ClassificationEvaluationMetrics.grp2idx(predicted)
        labels=ClassificationEvaluationMetrics.grp2idx(labels)
        a=zeros((unique(labels).size,unique(predicted).size))
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]):
                a[i,i2]=intersect1d(nonzero(labels==i)[0],nonzero(predicted==i2)[0]).size   
        a=double(a)
        n=labels.size
        mi=0
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]): 
                if a[i,i2]>0:
                    mi+=a[i,i2]*log((a[i,i2]*n)/(sum(a[i,:])*sum(a[:,i2])))
        mi=mi/log(unique(labels).size*unique(predicted).size)
        mi=mi/n
        return mi
     
    #Adjusted rand index
    #http://acl.ldc.upenn.edu/eacl2003/papers/main/p39.pdf
    @staticmethod
    def rand(predicted,labels):
        predicted=ClassificationEvaluationMetrics.grp2idx(predicted)
        labels=ClassificationEvaluationMetrics.grp2idx(labels)
        a=zeros((unique(labels).size,unique(predicted).size))
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]):
                a[i,i2]=intersect1d(nonzero(labels==i)[0],nonzero(predicted==i2)[0]).size
        cij=0
        a=double(a)
        for i in range(a.shape[0]):
            for i2 in range(a.shape[1]):
                if a[i,i2]>1:
                    cij+=combination(a[i,i2],2)
        ci=0
        for i in range(a.shape[0]):
            if sum(a[i,:])>1:
                ci+=combination(sum(a[i,:]),2)
        cj=0
        for i in range(a.shape[1]):
            if sum(a[:,i])>1:
                cj+=combination(sum(a[:,i]),2)
        cn=combination(double(labels.size),2)
        nominator=cij-((ci*cj)/cn)
        denominator=0.5*(ci+cj)-(ci*cj/cn)
        return nominator/denominator
    
    @staticmethod
    def _getPredictedAndLabels(clusters):
        labels=[]
        predicted=clusters
        for cluster in clusters:
            classBySize = defaultdict(int)
            for item in cluster: classBySize[item]+=1
            clusterType = sorted(classBySize.iteritems(),key=itemgetter(1), reverse=True)[0][0]
            labels.append([clusterType]*len(cluster))
        p,l=[],[]
        for pre in predicted: p+=pre
        for lab in labels: l+=lab
        return (array(p), array(l))
    
    @staticmethod
    def getValue(predicted, evaluationMethod):
        predicted, labels = ClassificationEvaluationMetrics._getPredictedAndLabels(predicted)
        return evaluationMethod(predicted, labels)
if __name__=="__main__":
    clusters = [['sports', 'sports', 'sports', 'sports'],
    ['entertainment', 'entertainment', 'sports', 'entertainment'],
    ['technology', 'technology', 'politics', 'technology'],
    ['politics', 'politics', 'politics', 'politics']
    ]
    
    print ClassificationEvaluationMetrics.getValue(clusters, ClassificationEvaluationMetrics.purity)