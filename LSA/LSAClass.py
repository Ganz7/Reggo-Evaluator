'''

Program: Coherence Evaluator
Stage: Intermediary

'''
import csv
from numpy import zeros
from scipy import linalg
from math import sqrt

# following needed for TFIDF
from math import log
from numpy import asarray, sum
import re


class LSA(object):
    def __init__(self, stopwords, ignorechars):     #Reads the training essays from the csv file
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0
        csvfile = csv.reader(open("training_set_rel3.csv", "rb"))  # Opens csv file
        i = 0;
        count = 0

        for row in csvfile:  # Reads the 1st 10 records
            if i == 0:
                i = i + 1
                continue
            if i == 100:
                break
            else:
                self.parse(row[2])  # 3rd column in the sheet has the essay
                count = count + 1;
                i = i + 1

    def parse(self, doc):                       #Checks for valid words and adds them to the dictionary

        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            temp=0
            for sw in self.stopwords:
                if w.lower()==sw.lower():
                    temp=1
                    break
            if temp==1:
                continue
            if w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):                            #Creates the word-by-document matrix

        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1

    def calc(self):                             #Singular Value Decomposition

        self.dim=10
        self.U, self.S, self.Vt = linalg.svd(self.A)

#     def TFIDF(self):
#         WordsPerDoc = sum(self.A, axis=0)
#         DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
#         rows, cols = self.A.shape
#         for i in range(rows):
#             for j in range(cols):
#                 self.A[i, j] = (self.A[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def printA(self):
        print '\nHere is the word-by-document matrix..'
        print self.A

    def printSVD(self):
        print '\nHere are the singular values'
        print self.S
        print '\nHere are the first 10 columns of the U matrix'
        print -1 * self.U[:, 0:10]
        #print 'Here are the first 3 rows of the Vt matrix'
        #print -1 * self.Vt[0:3, :]
        #print "\n\n"
    def calc_sentence(self,sentence):           #Finds the sentence vector of each sentence
        #print sentence.split()
        sent_vec=[]
        for count in range(self.dim):
            sent_vec.append(0)
        i=0
        for w in sentence.split():

            temp=0
            for sw in self.stopwords:
                if w.lower()==sw.lower():
                    temp=1
                    break
            if temp==1:
                continue
            else:

                if w in self.keys:
                    i = self.keys.index(w)
                    #print self.U[i]
                    for count in range(self.dim):
                        sent_vec[count] = sent_vec[count] + self.U[i][count]


        #print "Sentence Vector:"
        #print sent_vec
        return sent_vec

    def find_cosine(self,v1,v2):
        num=0
        densquare1=0
        densquare2=0
        for i in range(self.dim):
            num=num+(v1[i]*v2[i])
            densquare1=densquare1+(v1[i]*v1[i])
            densquare2=densquare2+(v2[i]*v2[i])
        den=sqrt(densquare1*densquare2)
        if den==0:
            den=1
        return (num/den)

    def calculateCoherence(self,text):
        sentences=re.split(r'[.!?]+', text)
        sentences.pop()
        total_coherence=0
        for i in range(0,len(sentences)-1):
            sent1_vec=self.calc_sentence(sentences[i])
            sent2_vec=self.calc_sentence(sentences[i+1])
            cosine=self.find_cosine(sent1_vec, sent2_vec)
            #print "Coherence btw '"+sentences[i]+"' and '"+sentences[i+1]+"'="+str(cosine)
            total_coherence=total_coherence+cosine
            avg_coherence = 0

        if(len(sentences)==0):
            avg_coherence = 0
        else:
            avg_coherence=total_coherence/ (len(sentences))
        return avg_coherence
