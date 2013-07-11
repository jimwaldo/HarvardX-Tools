#!/usr/bin/env python
'''
Takes a file mapping usernames to country and converts to userId to country

Used for an earlier version of the edX geolocation files, this takes a csv for a particular
course that mapped the username to the country indicated by the most-often used IP address
for the student and creates a file that maps from the userId to the country. 

This is largely obsoleted by the new format for a country mapping.

Created on May 4, 2013

@author: waldo
'''

import user
import csv
import os
import utils
import sys


def buildNameCountry(cfile):
    retDict = {}
    for [country, username] in cfile:
        retDict[username] = country
    return retDict

if len(sys.argv) > 3:
    cFileName = sys.argv[1]
    userFileName = sys.argv[2]
    clName = sys.argv[3]
else:
    cFileName = utils.getFileName('user name to country file')
    userFileName = utils.getFileName('user file')
    clName = raw_input("Please enter the name of the class : ")

cfile = csv.reader(open(cFileName, 'r'))
nameDict = buildNameCountry(cfile)
ufile = csv.reader(open(userFileName, 'r'))
userDict = user.builddict(ufile)


clfName = clName + '_id_country.csv'
outfile = csv.writer(open(clfName, 'w'))

users = userDict.keys()

outfile.writerow(['User id', 'Country'])
for u in users:
    userName = userDict[u].username
    if (userName in nameDict):
        country = nameDict[userDict[u].username]
        outfile.writerow([u, country])
    else:
        print ('unknown userName ' + userName)


