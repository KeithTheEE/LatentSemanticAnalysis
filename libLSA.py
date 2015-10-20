#!/usr/bin/env python

import os
import sys
import numpy
import math 
from sklearn.decomposition import ProjectedGradientNMF
import matplotlib.pyplot as plt

# Keith Murray

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    """
# Created by Albert Au Yeung (2010)
#
# An implementation of matrix factorization
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
accessed on Oct 14 2015
http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/
    """
    def progress():
	print("X"),
    Q = Q.T
    lastStep = 0
    #print("["),
    es = []
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
	es.append(e)
	#print e
	#if int(step/float(steps)*10) > lastStep:
	    #lastStep = int(step/float(steps)*10)
	    #progress()
    #if lastStep > 10:
	#for i in range(lastStep, 10):
	    #progress()
    #print("]")
    
    return P, Q.T, es

class termDocMatrix(object):
    def __init__(self, newThing="", docs=""):
	# Get term-document matrix
	# transormation/modified weighting of term-doc matrix 
	# dimensionality reduction
	# clustering of documents in reduced space
	self.wcThreshold = 2
	self.mD = {}
	self.tdm = []
	self.tdmraw = []
	self.termraw = []
	self.docs = []
	self.docsSize = []
	self.terms = []
	self.docCount = 0
        self.idfweight = False
	if newThing != "":
	    self.add(newThing, docs)
	self.P = []
	self.Q = []
	self.er = []
	self.idfs = []
	return
    def add(self, newThing, docs=""):
	def mergeDict(self, newD, docs=""):
	    # Grab doc count so far
	    docIndex = self.docCount
	    # Get the correct title
	    if docs == "":
		docs = docIndex
	    self.docs.append(docs)
	    # Add doc size (useful with tdmraw)
	    tdWeight = float(sum(newD.values()))
	    if tdWeight == 0:
		tdWeight = 1.
	    self.docsSize.append(tdWeight)
	    # Add newD to mD
	    for key in newD:
		#print key, newD[key]
		if key in self.mD:
		    if len(self.mD[key]) < self.docCount:
			for i in range(len(self.mD[key]), self.docCount):
			    self.mD[key].append(0.)
		    self.mD[key].append(newD[key]/float(tdWeight))
		else:
		    if self.docCount > 0:
			self.mD[key] = [0.]
		        for i in range(1, self.docCount):
			    self.mD[key].append(0.)
			self.mD[key].append(newD[key]/float(tdWeight))
		    else:
			self.mD[key] =  [newD[key]/float(tdWeight)]
	    self.docCount += 1
	    return
	    
	
	# Ok what was I just given?
	if type(newThing) == list:
	    # Shit.. Ok we can handle this, a list of what?
	    if len(newThing) > 0:
		if type(newThing[0]) == dict:
		    # Sweet, it's some dicts, merge them!
		    # Wait, what about the title var?
		    if (docs != "") and (type(docs) == list) and (len(docs) == len(newThing)):
			for i in range(len(newThing)):
			    mergeDict(self, newThing[i], docs[i])
		    else:
			for i in range(len(newThing)):
			    mergeDict(self, newThing[i])

		elif type(newThing[0]) in [float, long, int, str]:
		    # Well, I mean I don't see why numbers can't be LSA'ized
		    # Convert list to dict, then merge
		    newD = {}
		    for i in range(len(newThing)):
			if newThing[i] in newD:
			    newD[newThing[i]] += 1
			else:
			    newD[newThing[i]] = 1
		    mergeDict(self, newD)
		else:
		    raise(TypeError, "Elements of list are not valid inputs")

		

	elif type(newThing) == dict:
	    mergeDict(self, newD, docs)

	elif type(newThing) == str:
	    strList = newThing.split(" ")
	    newD = {}
	    for i in range(len(strList)):
		if strList[i].strip() in newD:
		    newD[strList[i].strip()] += 1
		else:
		    newD[strList[i].strip()] = 1
	    mergeDict(self, newD)
	return
    def weight_idf(self):
	# Now we're weighting it, booyea
	# There are two forms of weights applied here
	#   td: each term divided by the total terms from that doc
	#   idf: inverse document frequency: log(N/ni)
	#     if every doc has word ni, the it zeros out the row
	#     Rather than math it, check for it first
	self.idfweight = True
	for key in self.mD:
	    # Saving raw state allows matrix to grow w/o redoing everythign
	    self.termraw.append(key)
	    # This chunk is to check for the idf weight condition:
	    #   if every doc has the term, then it's not worth 'mathing'
	    #   and instead can be eliminated
	    idf = False
	    if len(self.mD[key]) < self.docCount:
		idf = True
		for i in range(len(self.mD[key]), self.docCount):
		    self.mD[key].append(0.)
	    # Saving raw matrix
	    self.tdmraw.append(self.mD[key])
	    # Scan row for a zero
	    if idf == False:
		for i in range(len(self.mD[key])):
		    if self.mD[key][i] == 0:
			idf = True
			break
	    # CURRENTLY AN ERROR DUE TO TD WEIGHTING EARLIER
	    if (len(filter(None, self.mD[key])) >= self.wcThreshold) and idf == True:
		self.terms.append(key)
		self.tdm.append(self.mD[key])
	
	# Ok now it's actually time to start weighting
	self.tdm = numpy.array(self.tdm)
	#print len(self.tdm)
	for i in range(len(self.tdm)):
	    #print self.terms[i]
	    ni = float(numpy.count_nonzero(self.tdm[i]))
	    if ni == 0:
		raise ValueError("ARG HOW ARE THERE NO NON ZERO ELIMENTS")
	    #print ni, self.docCount
	    idfValue = math.log(self.docCount/ni)
	    self.tdm[i] = self.tdm[i] * idfValue
	    self.idfs.append(idfValue)
	    
	return

    def svd(self):
	return

    def nmf(self, k):
	
	nmf = ProjectedGradientNMF(n_components=k, max_iter=200)
	print len(self.tdm), len(self.tdm[0])
	P = nmf.fit_transform(self.tdm)
	Q = nmf.components_.T
	print len(P), len(P[0]),  len(Q), len(Q[0])
	#print nmf.components_
	#print nmf
	# R     : a matrix to be factorized, dimension N x M
	# P     : an initial matrix of dimension N x K
	# Q     : an initial matrix of dimension M x K
	#P = numpy.random.random(size=(len(self.tdm), k))
	#Q = numpy.random.random(size=(len(self.tdm[0]), k))
	#P, Q, es = matrix_factorization(self.tdm, P, Q, k, steps=5000, alpha=0.0002, beta=0.02)
	self.P = P
	self.Q = Q
	self.er = nmf.reconstruction_err_
	print "\tError: ", self.er
	return P, Q
 
    def saveParts(self, location=""):
	# Check Location
	if location != "":
	    if location[-1] != "/":
		location = str(location) + "/"
	    if not os.path.exists(location): os.makedirs(location)
	# Save Terms
	termSet = open(str(location) + "terms.lst", 'w')
	for i in range(len(self.terms)):
	    termSet.write(str(self.terms[i]) +"\n")
	termSet.close()
	# Save Docs
	docSet = open(str(location) + "docs.lsd", 'w')
	for i in range(len(self.docs)):
	    docSet.write(str(self.docs[i]) +"\n")
	docSet.close()
	tdmR = open(str(location) + "tdmRaw.lsm", 'w')
	for i in range(len(self.tdmraw)):
	    for j in range(len(self.tdmraw[i])):
		tdmR.write(str(self.tdmraw[i][j]) + "\t")
	    tdmR.write("\n")
	tdmR.close()
	p = open(str(location) + "Pmatrix.lsp", 'w')
	for i in range(len(self.P)):
	    for j in range(len(self.P[i])):
		p.write(str(self.P[i][j]) + "\t")
	    p.write("\n")
	p.close()
	q = open(str(location) + "Qmatrix.lsq", 'w')
	for i in range(len(self.Q)):
	    for j in range(len(self.Q[i])):
		q.write(str(self.Q[i][j]) + "\t")
	    q.write("\n")
	q.close()
	idfs = open(str(location) + "idf.lsi", 'w')
	for i in range(len(self.idfs)):
	    idfs.write(str(self.idfs[i]) + "\n")
	idfs.close()

	'''
	plt.plot(self.er)
	plt.xlabel("Itteration")
	plt.ylabel("Error")
	plt.title("Error During NMF: Final = " + str(self.er[-1]))
	plt.savefig(str(location) + "Error.pdf", bbox_inches='tight')
	plt.savefig(str(location) + "Error.png", bbox_inches='tight')
	plt.close()
	'''
	# AMI DIST MAT
	return
	    
	
	    


    def __repr__(self):
	if self.idfweight == False:
	    a = "\t"
	    for i in range(len(self.docs)):
	        a = a +'"'+ str(self.docs[i]) +'"'+ "\t"
	    a = a + "\n"
	
	    for key in self.mD:
	        a = a +'"'+ key +'"'+ "\t"
	        for i in range(self.docCount):
		    if i < len(self.mD[key]):
		        a = a + str(self.mD[key][i]) + ",\t"
		    else:
		        a = a + "0.0,\t"
	        a = a + "\n"
	else:
	    a = "\t"
	    for i in range(len(self.docs)):
	        a = a +'"'+ str(self.docs[i]) +'"'+ "\t"
	    a = a + "\n"
	    for i in range(len(self.terms)):
		a = a +'"'+  self.terms[i] + '"\t'
		for j in range(self.docCount):
		    a = a + str(self.tdm[i][j]) + ",\t"
		a = a + "\n"
	#msg = str(a)
	return a


   

