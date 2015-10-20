#!/usr/bin/env python

import os
import sys
import numpy
import gzip,cPickle
import math

import libLSA

# Keith Murray

   


def save(D, filename):
    file = gzip.open(filename+'.gzip', 'w')
    cPickle.dump(D, file)
    file.close()

def load(filename):
    file = gzip.open(filename+'.gzip')
    #KEITH EDIT
    #file = gzip.open(filename)
    D=cPickle.load(file)
    file.close()
    return D
    

def getTweetsToDict(lsa):
    #dSet = open("/home/keith/Documents/filesForProgramming/Twitter/lsaDB/earthquake/tweetProof.txt", 'r')
    #clnDS = open("/home/keith/Documents/filesForProgramming/Twitter/lsaDB/earthquake/tweetProofC.txt", 'w')
    dSet = open("toyData.txt", 'r')
    clnDS = open("toyDataC.txt", 'w')
    for line in dSet:
	if line not in ["\n", ""]:
	    lsa.add(line.strip().lower())
	    clnDS.write(line.lower())
    dSet.close()
    clnDS.close()
    return lsa
    
    
def euclidean(a, b) :
    i = 0
    x = 0
    y = 0
    difference = 0
    euclideanDistance = 0
    sumEuc = 0
    for i in range(len(a)) :
        x = float(a[i])
        y = float(b[i])
        
        difference = (x - y)
        sumEuc += difference*difference
    euclideanDistance = math.sqrt(sumEuc)
    '''
    if ( euclideanDistance != 0) :
        euclideanDistance = 1 / euclideanDistance
    else :
        euclideanDistance = 1
    '''
    return euclideanDistance
def Correlation(a, b):

    i = 0
    j = 0
    meanA = 0
    meanB = 0
    for i in range(len(a)) :
        meanA = meanA + float(a[i])
    for j in range(len(b)) :
        meanB = meanB + float(b[j])

    meanA = float(meanA)/len(a)
    meanB = float(meanB)/len(b)
    
    k = 0
    l = 0
    A = 0
    Asqrt = 0
    B = 0
    Bsqrt = 0
    dotProduct = 0
    denom = 0
    distance = 0

    formatDistance = 0

    for k in range(len(a)) :
        A = float(a[k]) #- meanA
        B = float(b[k]) #- meanB

        dotProduct = dotProduct + (A - meanA)*(B - meanB)
        
        Asqrt = Asqrt + ((A - meanA) * (A - meanA))
        Bsqrt = Bsqrt + ((B - meanB) * (B - meanB)) 

   # print Asqrt
   # print Bsqrt
    Asqrt = math.sqrt(Asqrt)
    Bsqrt = math.sqrt(Bsqrt)
   # print Asqrt
   # print Bsqrt
    
    
    denom = Asqrt * Bsqrt
    if denom == 0:
	denom = .000000001
    distance = float(dotProduct)/denom

    correlationDistance = 1 - distance 
        
    return correlationDistance


def nspectDocs(mat, filename='nSpectDM.dm'):
    print len(mat)
    dm = [[0.0 for y in range(len(mat))] for x in range(len(mat))]
    dmM = 0
    for i in range(len(mat)):
	for j in range(len(mat)):
	    if i != j:
		dm[i][j] = euclidean(mat[i], mat[j])
		if dm[i][j] > dmM:
		    dmM = dm[i][j]
    dm = numpy.array(dm)
    dm = dm/float(dmM)
    #dmf = open('/home/keith/Documents/filesForProgramming/Twitter/lsaDB/earthquake/nSpectDM.dm', 'w')
    dmf = open(filename, 'w')
    dmf.write(str(len(mat)) + "\n")
    for i in range(len(mat)):
	dmf.write("Seq" + str(i) + '\t')
	for j in range(len(mat)):
	    dmf.write(str.format("{0:.10f}", dm[i][j]))
	    if j != len(mat):
		dmf.write('\t')
	dmf.write('\n')
    dmf.close()

def cluster(count, lsa):
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=count, init='random', n_init=1, verbose=1)
    km.fit(lsa.P)
    tData = open("toyDatP.dl", 'w')
    for i in range(len(km.labels_)):
	tData.write(str(km.labels_[i]) + " 0 4\n")
    tData.close()

def main():
    # Get term-document matrix
    # transormation/modified weighting of term-doc matrix 
    # dimensionality reduction
    # clustering of documents in reduced space
    lsa = libLSA.termDocMatrix()
    lsa = getTweetsToDict(lsa)
    print "\tAdded to Dict\n\tidf now"
    lsa.weight_idf()
    #print lsa.terms, len(lsa.mD.keys())
    print "\tnfm"
    #save(lsa, "/home/keith/Documents/filesForProgramming/Twitter/lsaDB/tornado/dataStructSave")
    #lsa = load("/home/keith/Documents/filesForProgramming/Twitter/lsaDB/tornado/dataStructSave")
    #print "\tloaded"
    P, Q = lsa.nmf(20)
    print "\tsaving"
    #save(lsa, "/home/keith/Documents/filesForProgramming/Twitter/lsaDB/earthquake/dataStructSave")
    save(lsa, "dataStructSave")
    #lsa.saveParts("/home/keith/Documents/filesForProgramming/Twitter/lsaDB/earthquake/")
    lsa.saveParts()
    #lsa = load("quicks")
    print "\tnSpect DM Loading"
    nspectDocs(lsa.Q)
    nspectDocs(lsa.P, filename='nSpectDMP.dm')
    cluster(15, lsa)
    '''
    temp = open("lsa.xlsx", 'w')
    temp.write(lsa.__repr__())
    temp.close()
    '''

    return

main()


































