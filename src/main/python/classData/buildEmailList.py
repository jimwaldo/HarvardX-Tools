#!/usr/bin/env python
"""
Builds a csv file of First Name, Last Name, email address for a course

This file needs to be run from a directory in which the users.csv and profiles.csv files
exist. When run, it produces a mailAddresses.csv file with the above format. It will only
include entries for students that are in the user.csv file. If there is a student in the
users.csv file but not in the profiles.csv file, the student's name will read "Missing
 Profile"

Created on Nov 13, 2013

@author: waldo
"""
import classData.userprofile as userp
from classData import user
import sys
import csv

def split(name):
    spIn = name.rfind(' ')
    first = name[ :spIn]
    last = name[spIn + 1: ]
    return [first, last]

if __name__ == '__main__':
    csv.field_size_limit(sys.maxsize)
    ufile = csv.reader(open('users.csv','r'))
    udict = user.builddict(ufile)
    pfile = csv.reader(open('profiles.csv', 'r'))
    pdict = userp.builddict(pfile)
    
    outfile = csv.writer(open('mailAddresses.csv','w'))
    
    for uid in iter(udict):
        if uid in pdict:
            name = pdict[uid].name
        else :
            name = 'Missing Profile'
        [first, last] = split(name)
        outfile.writerow([first, last, udict[uid].email])
