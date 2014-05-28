#!/usr/bin/env python

'''
Created on May 28, 2014

@author: waldo
'''
import sys
import csv
import utils

def makeDict(ids, infile):
    retDict = {}
    for line in infile:
        for i in ids:
            if line[i] in retDict:
                retDict[line[i]] += 1
            else:
                retDict[line[i]] = 1
    return retDict

def makeCountDict(anonDict):
    retDict = {}
    for i in iter(anonDict):
        c = anonDict[i]
        if c in retDict:
            retDict[c] += 1
        else:
            retDict[c] = 1
    return retDict

if __name__ == '__main__':
#     idFields = [6,7,8,9,13]
    idFields = [7]
    fname = utils.getFileName('data file to test')
    fin = open(fname, 'rU')
    fread = csv.reader(fin)
    
    fread.next()
    anonDict = makeDict(idFields, fread)
    print len(anonDict)
    
    counts = makeCountDict(anonDict)
    citer = iter(counts)
    for i in citer:
        if i < 6:
            print i, counts[i]
        
    