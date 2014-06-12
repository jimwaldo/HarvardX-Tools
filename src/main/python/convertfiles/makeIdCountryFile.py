#!/usr/bin/env python
"""
Takes a file mapping usernames to country and converts to userId to country

Used for an earlier version of the edX geolocation files, this takes a csv for a particular
course that mapped the username to the country indicated by the most-often used IP address
for the student and creates a file that maps from the userId to the country. This was the
format that was given to us by edX, and it was class-centric; hence the notion of naming 
the output file with the classname followed by _id_country.csv. 

This is largely obsoleted by the new format for a country mapping.

Created on May 4, 2013

@author: waldo
"""

from classData import user
import csv
import utils
import sys


def buildNameCountry(cfile):
    """
    Take an open .csv file with format country, username and create a dictionary
    indexed by username with value country
    """
    retDict = {}
    for [country, username] in cfile:
        retDict[username] = country
    return retDict

if __name__ == '__main__':
    if len(sys.argv) > 3:
        cFileName = sys.argv[1]
        userFileName = sys.argv[2]
        lName = sys.argv[3]
    else:
        cFileName = utils.getFileName('Name of user name to country file : ')
        userFileName = utils.getFileName('Name of user file : ')
        clName = utils.getNewFileName('Name of class for the output file : ')

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


