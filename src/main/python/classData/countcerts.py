#!/usr/bin/env python
"""
Totals the number of students who passed, did not pass, or are restricted from a certificate

Goes over a certificates file for a course that has completed, finding
the total number of students, the number who were awarded a certificate,
those that did not receive a certificate, and those that are restricted 
from receiving a certificate (because of being in an embargoed country)
Created on Feb 20, 2013

@author: waldo
"""

import certificates
import csv
import sys

if __name__ == '__main__':
    infile = csv.reader(open(sys.argv[1], 'r'))
    infile.next()
    certDict = certificates.builddict(infile)
    passed = unfinished = restrict = total = unknown = 0
    citer = iter(certDict)
    for c in citer:
        if certDict[c].status == "downloadable":
            passed += 1
        elif certDict[c].status == 'notpassing':
            unfinished += 1
        elif certDict[c].status == 'restricted':
            restrict += 1
        else:
            print certDict[c].status
            unknown += 1
        total += 1
    
    print "Total records = " + str(total)
    print "Total passed = " + str(passed)
    print 'Total not passing = ' + str(unfinished)
    print 'Total restricted = ' + str(restrict)
    print 'Total unknown = ' + str(unknown)