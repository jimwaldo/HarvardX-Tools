#!/usr/bin/env python

'''
Created on May 28, 2014

@author: waldo
'''
import operator
import csv
import utils

'''
Concatenate a set of fields together to build an overall key

This is a simple approach to determining k-anonymity, in which all
of the fields of interest are concatenated as a single key. The 
ids coming in should be a list of indexes into the fields in the dataLine.
These will be concatenated in order to form a new key. Note that this 
currently assumes that all of the data fields are strings. 

'''
def buildKey(ids, dataLine):
    retKey = ''
    for i in ids:
        retKey += dataLine[i]
        
    return retKey

'''
Create and return a dictionary keyed by a concatenation of fields with value the number
of entries containing all and only those fields.

Taking a list of indexes into a line of a (csv) file and an open csv.reader(), build a 
dictionary that is keyed by the string concatenation of the fields in the index with
value the number of times a line containing just those fields in those indexes occurs. Return
the dictionary to the caller.

'''
def makeDict(ids, infile):
    retDict = {}
    for line in infile:
        keyAnon = buildKey(ids, line)
        if keyAnon in retDict:
            retDict[keyAnon] += 1
        else:
            retDict[keyAnon] = 1
  
    return retDict

'''
When run stand-alone, this script will query for a filename and a level of anonymity
to check for the externally-connected data fields in the .csv file. The user will also
be prompted for either a summary of the anonymity level (in which case only the number
of records that fail to be at least anonymous to the level indicated) will be printed, or
a full report, in which case the concatenation of fields that allow identification finer
than the level entered will be printed. Note that the indexes of the fields that can be
linked to external properties is hard-coded at the moment; it would be good to have a more
flexible mechanism for this but finding one that is not error prone is difficult.

'''
if __name__ == '__main__':
    idFields = [0,6,7,8,9,17]
    fname = utils.getFileName('data file to test')
    kanon = utils.getIntVal('Enter value of k to test : ')
    full = utils.getStringVal('Enter s for summary, f for full report : ', ['s', 'f'])
    fin = open(fname, 'rU')
    fread = csv.reader(fin)
    
    totals = []
    for i in range(0,kanon):
        totals.append(0)
        
    fread.next()
    anonDict = makeDict(idFields, fread)
    sortedDict = sorted(anonDict.iteritems(), key=operator.itemgetter(1))
    for k,v in sortedDict:
        if v < kanon:
            totals[v-1] += 1
            if full == 'f':
                print v, k
    for i in range(0,kanon-1):
        print 'Number of buckets with', i+1, 'entries is', totals[i]

        
    