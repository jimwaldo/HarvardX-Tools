#!/usr/bin/env python

"""
Created on Apr 22, 2013

Create a file of FERPA de-identified demographic data

The program takes five arguments:
    A string that names the course;
    A file containing the userprofile data, in CSV format;
    A file containing the user data, in CSV format;
    A file containing the mapping from usernames to countries;
    A file containing the users who received certificates (optional)
    

@author: waldo
"""

import sys
import csv
from classData import userprofile as prof
from classData import user
from classData import certificates as cs
from classData import ipGeoloc as geo


if (len(sys.argv) < 2):
    print('Usage: buildAnonProfile.py courseName profileFile userFile countryFile certFile')
    sys.exit()
    
csv.field_size_limit(1000000)

out_name = sys.argv[1] + 'anonProfile.csv'
o1 = csv.writer(open(out_name, 'w'))

ufile = csv.reader(open(sys.argv[2], 'r'))
uprof = prof.builddict(ufile)

udfile = csv.reader(open(sys.argv[3], 'r'))
udict = user.builddict(udfile)

countryFile = csv.reader(open(sys.argv[4], 'r'))
locDict = geo.builddict(countryFile)

certs = False
if (len(sys.argv) > 5):
    certfile = csv.reader(open(sys.argv[5], 'r'))
    certDict = cs.builddict(certfile)
    certs = True
    

students = uprof.keys()
for s in students:
    p = uprof[s]
    if (s in udict):
        usrName = udict[s].username
        if (usrName in locDict):
            loc = locDict[usrName]
        else:
            loc = ''
    else:
        loc = ''
        
    if (certs):
        o1.writerow([p.gender, p.yob, p.ledu, p.goal, loc, (p.user_id in certDict)])
    else: 
        o1.writerow([p.gender, p.yob, p.ledu, p.goal, loc])


        

