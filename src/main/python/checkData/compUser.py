#!/usr/bin/env python
'''
A simple script to compare two user files and a certificates file

Generates a report of users differences between multiple user files,
with the additional check to see if those users that are in one of the
files but not the other are in the certificates files. This script assumes
that the certificates file being used is in the directory in which the
script is run, and takes as arguments the file names of the two user
files to be compared.
'''

import csv
import sys
from classData import certificates, user

if __name__ == '__main__':
    f1 = csv.reader(open(sys.argv[1], 'r'))
    f2 = csv.reader(open(sys.argv[2], 'r'))
    f3 = csv.writer(open('additions.csv', 'w'))
    f4 = csv.reader(open('certificates.csv', 'r'))
    f3.writerow(['id', 'in certificate file'])
    f3.writerow(['User ids in first file, not in second'])
    u1 = user.builddict(f1)
    u2 = user.builddict(f2)
    cdict = certificates.builddict(f4)
    for key in u1.iterkeys():
        if u1[key].id not in u2:
            if key in cdict:
                f3.writerow([key, 'Yes'])
            else:
                f3.writerow([key, 'No'])
    
    f3.writerow(['User ids in second file, not in first'])
    for key in u2.iterkeys():
        if u2[key].id not in u1:
            if key in cdict:
                f3.writerow([key, 'Yes'])
            else:
                f3.writerow([key, 'No'])




