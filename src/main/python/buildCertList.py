#!/usr/bin/env python
'''
Builds a dictionary of all of the certificates a user has been
considered for, indexed by the user id.

It is run in a directory which has all of the courses. Each course
directory should have a particular date dump

Created on October 11, 2013

@author: lazovich
'''

import certificates
from certificates import cert
import csv
import sys
import glob


def processCerts(dir):
    try:
        f = open(dir+"/certificates.csv", 'r')
    except IOError:
        return None

    infile = csv.reader(f)
    certDict = certificates.builddict(infile)

    return certDict


def mergeCertDicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            obj1 = dict1[key]
            obj2 = dict2[key]
            merged = None

            if isinstance(obj1, cert):
                merged = [obj1, obj2]
            else:
                obj1.append(obj2)
                merged = obj1

            dict1[key] = merged
        else:
            dict1[key] = dict2[key]

    return dict1


def main():
    if len(sys.argv) != 2:
        print "Usage: buildCertList.py dir_name"
        return 1

    indir = sys.argv[1]
    dirList = glob.glob(indir+"/"+"*x*20*")

    allCerts = {}

    # Iterate over all courses
    for dir in dirList:
        fList = glob.glob(dir+"/"+"*20*")

        # Iterate over all dumps
        allCourseCerts = {}

        for f in fList:
            certDict = processCerts(f)

            # Overwrites cert from earlier dumps
            # if user is already there
            allCourseCerts.update(certDict)

        mergeCertDicts(allCerts, allCourseCerts)
        print "%s: %d " % (dir, len(allCourseCerts))

    print len(allCerts)
    ct = 0

    for key in allCerts:
        if not isinstance(allCerts[key], cert):
            if len(allCerts[key]) == 5:
                ct += 1

    print "Students in all 5: %d" % ct

if __name__ == '__main__':
    main()
