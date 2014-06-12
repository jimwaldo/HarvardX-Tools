#!/usr/bin/env python
"""
Builds a dictionary of all of the certificates a user has been
considered for, indexed by the user id.

It is given a directory which has all of the courses. Each course
directory should have at least one date dump

Writes a FullCertList.json file to the given directory

Created on October 11, 2013

@author: lazovich
"""


from classData.certificates import cert, CertEncoder, builddict
import csv
import sys
import glob
import json


def processCerts(direct):
    """
    Construct a dictionary of certificate recipients for a course,
    given the directory of the certificates.csv file

    Parameters
    -----------
    direct: A string corresponding to the directory of the certificates.csv
    """

    try:
        f = open(direct+"/certificates.csv", 'r')
    except IOError:
        return None

    infile = csv.reader(f)
    certDict = builddict(infile)

    return certDict


def mergeCertDicts(dict1, dict2):
    """
    Take two dictionaries and merge them. Combines values with the
    same key as a list

    Parameters
    -----------
    dict1, dict2: dictionaries to be merged
    """

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
    for direct in dirList:
        fList = glob.glob(direct+"/"+"*20*")

        # Iterate over all dumps
        allCourseCerts = {}

        for f in fList:
            certDict = processCerts(f)

            # Overwrites cert from earlier dumps
            # if user is already there
            allCourseCerts.update(certDict)

        mergeCertDicts(allCerts, allCourseCerts)

    outfile = open(indir + "/" + "FullCertList.json", 'w')
    outfile.write(json.dumps(allCerts, cls=CertEncoder))


if __name__ == '__main__':
    main()
