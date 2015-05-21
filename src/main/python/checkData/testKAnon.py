#!/usr/bin/env python

"""
Tests whether a file (in .csv format) with each line, consisting of data about a single student,
is anonymous with to a particular level of k.

This program will take a set of fields in each line (hard coded, at the moment) and will check to
insure that there are at least k other lines with the same values for those fields. The fields 
selected should be all those that can be used to re-identify a student. The program will ask for the
data file to test and the level of k to test. 

The program can be run in either full or summary mode. In summary mode, the program will print the
number of lines that would violate the level of k specified. In full mode, all of sets of properties
that would violate the level of k are printed out, so that one can see what properties might need
to be smeared.

Created on May 28, 2014

@author: waldo
"""
import operator
import csv, sys
import utils
def buildKey(ids, dataLine):
    """
    Concatenate a set of fields together to build an overall key

    This is a simple approach to determining k-anonymity, in which all
    of the fields of interest are concatenated as a single key. The 
    ids coming in should be a list of indexes into the fields in the dataLine.
    These will be concatenated in order to form a new key. Note that this 
    currently assumes that all of the data fields are strings. 

    """
    retKey = ''
    for i in ids:
        retKey += dataLine[i]
        
    return retKey

def makeDict(ids, infile):
    """
    Create and return a dictionary keyed by a concatenation of fields with value the number
    of entries containing all and only those fields.

    Taking a list of indexes into a line of a (csv) file and an open csv.reader(), build a 
    dictionary that is keyed by the string concatenation of the fields in the index with
    value the number of times a line containing just those fields in those indexes occurs. Return
    the dictionary to the caller.

    """
    retDict = {}
    for line in infile:
        keyAnon = buildKey(ids, line)
        if keyAnon in retDict:
            retDict[keyAnon] += 1
        else:
            retDict[keyAnon] = 1
  
    return retDict

if __name__ == '__main__':
    """
    When run stand-alone, this script will query for a filename and a level of anonymity
    to check for the externally-connected data fields in the .csv file. The user will also
    be prompted for either a summary of the anonymity level (in which case only the number
    of records that fail to be at least anonymous to the level indicated) will be printed, or
    a full report, in which case the concatenation of fields that allow identification finer
    than the level entered will be printed. Note that the indexes of the fields that can be
    linked to external properties is hard-coded at the moment; it would be good to have a more
    flexible mechanism for this but finding one that is not error prone is difficult.

    The id fields that could connect to the outside are 0 -> course_id, 6 -> final_cc_cname,
    7 -> LoE, 8 -> YoB, 9 -> gender, and 17 -> nforum_posts]
    """
    idFields = [0,6,7,8,9,17]
    if len(sys.argv) < 4:
        fname = utils.getFileName('data file to test')
        kanon = utils.getIntVal('Enter value of k to test : ')
        full = utils.getStringVal('Enter s for summary, f for full report : ', ['s', 'f'])
    else:
        fname = sys.argv[1]
        kanon = int(sys.argv[2])
        full = sys.argv[3]
        
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

        
    
