#!/usr/bin/env python

import os
import sys
import numpy

import libLSA

# Keith Murray

   

def getTweetsToDict(infile):
    pass
    





def main():
    # Get term-document matrix
    # transormation/modified weighting of term-doc matrix 
    # dimensionality reduction
    # clustering of documents in reduced space

    lsa = libLSA.termDocMatrix("a b b c c c")
    lsa.add("a a a b b b b d d d d d")
    lsa.add("transormation/modified weighting of a term-doc matrix")
    print "PYTHON"
    print lsa
    lsa.weight_idf()
    print lsa
    '''
    temp = open("lsa.xlsx", 'w')
    temp.write(lsa.__repr__())
    temp.close()
    '''

    return

main()


































