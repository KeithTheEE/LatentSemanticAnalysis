#!/usr/bin/env python

import os
import sys
import numpy
import math 
import sklearn

# Keith Murray

class termDocMatrix(object):
   def __init__(self, newThing, docs=""):
	# Get term-document matrix
	# transormation/modified weighting of term-doc matrix 
	# dimensionality reduction
	# clustering of documents in reduced space
	self.mD = {}
	self.tdm = []
	self.tdmraw = []
	self.termraw = []
	self.docs = []
	self.docsSize = []
	self.terms = []
	self.docCount = 0
        self.idfweight = False
	self.add(newThing, docs)
	return
   def add(self, newThing, docs=""):
	def mergeDict(self, newD, docs=""):
	    # Grab doc count so far
	    docIndex = self.docCount
	    # Get the correct title
	    if docs == "":
		docs = docIndex
	    self.docs.append(docs)
	    # Add doc size (useful wiht tdmraw)
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
		    self.mD[key].append(newD[key]/tdWeight)
		else:
		    if self.docCount > 0:
			self.mD[key] = [0.]
		        for i in range(1, self.docCount):
			    self.mD[key].append(0.)
			self.mD[key].append(newD[key]/tdWeight)
		    else:
			self.mD[key] =  [newD[key]/tdWeight]
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
	    if idf == True:
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


   

