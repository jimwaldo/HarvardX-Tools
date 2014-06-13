#!/usr/bin/env python
"""
A simple interactive program to compare the ids in a file with those in a 
certificates file

This program will prompt the user for the name of a csv file containing
only user ids, and a csv of a certificates file, and see if there are any 
ids in the first file that correspond to entries in the certificates file.
"""


import csv
import sys
from classData import certificates
import utils

if __name__ == '__main__':
    if len(sys.argv) > 2:
        f1name = sys.argv[1]
        f2name = sys.argv[2]
    else:
        f1name = utils.getFileName('Enter csv file with ids : ')
        f2name = utils.getFileName('Enter certificates csv file name : ')
    f1 = csv.reader(open(f1name, 'r'))
    f2 = csv.reader(open(f2name, 'r'))
    certdict = certificates.builddict(f2)
    f1.readrow()
    for [ident] in f1:
        if ident in certdict:
            print 'found new identifier ' + ident + ' in certificates file'

    
