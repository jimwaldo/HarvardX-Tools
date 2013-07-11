#!/usr/bin/env python

'''
Construct a global user list for all of the courses offered

When run in a directory that contains as sub-directories the data files for
all of the classes, will get the user.csv file from each of the sub-directories
and construct a pair of dictionary of all of the users listed in those files. 
One dictionary will map from userId=> username, the other from username=> userId.
Users in more than one users.csv file will only be listed once. The result is 
written to a pair of files; globalid2name.csv (for the id=>name dictionary) and
globalname2id.csv (for the username=> id dictionary). Note that each of these
files is written with a first-line header that should be discarded if the files
are read for processing.

The file also contains a pair of methods that can be used to reconstruct the
dictionaries from the files.

Created on Jul 5, 2013

@author: waldo
'''

import glob
import csv
import user

def readId2Name(fin):
    '''
    Reconstruct a global id=>username dictionary from an open csv file
    
    Reads the globalId2Name file (or equivalent) and constructs an id=>username
    dictionary. Input is an open csv.reader file such as the one constructed
    by the main method of this module. Returns a dictionary of id=>username
    '''
    retDict = {}
    fin.readrow()
    for iden, name in fin:
        retDict[iden] = name
    return retDict

def readName2Id(fin):
    '''
    Reconstructs a gloval username=>id dictionary from an open csv file
    
    Reads the globalName2Id file (or equivalent) and constructs a username=>id
    dictionary. Input is an open csv.reader files such as the one constructed
    by the main method of this module. Returns a dictionary of username=>id
    '''
    retDict= {}
    fin.readrow()
    for name, iden in fin:
        retDict[name] = iden
    return retDict

if __name__ == '__main__':
    pass

ulist = glob.glob('*/users.csv')
idDict = {}
nameDict = {}

for fname in ulist:
    fin = open(fname, 'r')
    fcsv = csv.reader(fin)
    udict = user.builddict(fcsv)
    for u in iter(udict):
        idDict[u] = udict[u].username
        nameDict[udict[u].username] = u
    fin.close()
    
idOut = csv.writer(open('globalid2name.csv', 'w'))
idOut.writerow(['User ID', 'User Name'])
for i in iter(idDict):
    idOut.writerow([i, idDict[i]])
    
nameOut = csv.writer(open('globalname2id.csv', 'w'))
nameOut.writerow(['User Name', 'User ID'])
for n in iter(nameDict):
    nameOut.writerow([n, nameDict[n]])
