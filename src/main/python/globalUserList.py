#!/usr/bin/env python

'''
Construct a global user list for all of the courses offered

When run in a directory that contains as sub-directories of sub-directories the data files for all of the classes, will
get the user.csv file from each of the sub-directories and construct a pair of dictionary of all of the users listed in
those files. One dictionary will map from userId=> username, the other from username=> userId. Users in more than one
users.csv file will only be listed once. The result is written to a pair of files; globalid2name.csv (for the id=>name
dictionary) and globalname2id.csv (for the username=> id dictionary). Note that each of these files is written with a
first-line header that should be discarded if the files are read for processing.

During the construction of the global maps, the function will also look for duplicate mappings
from id to name or from name to id, and will construct a dictionary for each that will be
keyed by the item with multiple mappings and have as value a list of the mappings. If no
duplicates are found, a message to that effect will be printed to the console at the end of 
the run; if any are found they are written to a .csv file in the directory in which the
program was run (nameDups.csv or idDups.csv)

The file also contains a pair of methods that can be used to reconstruct the
dictionaries from the files.

Created on Jul 5, 2013

@author: waldo
'''

import glob
import csv
import user

def addDup(inDict, key, oval, nval):
    if key in inDict:
        inDict[key].append(nval)
    else:
        inDict[key]= [oval, nval]
        
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
    Reconstructs a global username=>id dictionary from an open csv file
    
    Reads the globalName2Id file (or equivalent) and constructs a username=>id
    dictionary. Input is an open csv.reader files such as the one constructed
    by the main method of this module. Returns a dictionary of username=>id
    '''
    retDict= {}
    fin.readrow()
    for name, iden in fin:
        retDict[name] = iden
    return retDict

def main():
    ulist = glob.glob('*/*/users.csv')
    idDict = {}
    nameDict = {}
    dupNameDict = {}
    dupIdDict = {}

    for fname in ulist:
        fin = open(fname, 'r')
        fcsv = csv.reader(fin)
        udict = user.builddict(fcsv)
        for u in iter(udict):
            if u not in idDict:
                idDict[u] = udict[u].username
            elif idDict[u] != udict[u].username:
                addDup(dupNameDict, u, idDict[u], udict[u].username)
            if udict[u].username not in nameDict:   
                nameDict[udict[u].username] = u
            elif nameDict[udict[u].username] != u:
                addDup(dupIdDict, udict[u].username, nameDict[udict[u].username], u)
    fin.close()
    
    idOut = csv.writer(open('globalid2name.csv', 'w'))
    idOut.writerow(['User ID', 'User Name'])
    for i in iter(idDict):
        idOut.writerow([i, idDict[i]])
    
    
    nameOut = csv.writer(open('globalname2id.csv', 'w'))
    nameOut.writerow(['User Name', 'User ID'])
    for n in iter(nameDict):
        nameOut.writerow([n, nameDict[n]])

    if len(dupNameDict) > 0:
        nameDupOut = csv.writer(open('nameDups.csv', 'w'))
        for u in iter(dupNameDict):
            nameDupOut.writerow[u, dupNameDict[u]]
    else:
        print("No duplicate names found")       
        
    if len(dupIdDict) > 0:
        idDupOut = csv.writer(open('idDups.csv', 'w'))
        for u in iter(dupIdDict):
            idDupOut.write([u, dupIdDict[u]])
    else:
        print("No duplicate ids found")

if __name__ == '__main__':
    main()

    
