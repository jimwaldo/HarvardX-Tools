#!/usr/bin/env python

'''
Build a cumulative class roster for a class

Run from a directory that contains all of the weekly dumps of data for a class from 
edX, this script will build a roster for all students who have ever shown up in the
weekly profiles.csv files. The roster will include student id, name, country, age,
education level, and gender. This should allow us to see all students in a course,
even those that have withdrawn, as long as they remained in the course for a single
data dump.

Created on Jul 11, 2013
Modified on Jul 28, 2013

@author: waldo
'''

import glob
import csv
import sys
import utils
import buildClassRoster as bcr
import demographics.userprofile as prof
import ipGeoloc as geo
import user

def main(locname, relLoc="./"):
    csv.field_size_limit(sys.maxsize)
    locD = geo.readIdToLoc(locname)
    flist = glob.glob(relLoc + '20*')
    fname = flist.pop()
    fin = csv.reader(open(fname + '/profiles.csv', 'r'))
    pDict = prof.builddict(fin)
    uin = csv.reader(open(fname +'/users.csv', 'r'))
    uDict = user.builddict(uin)
    fullR = bcr.buildRosterDict(pDict, uDict, locD)

    for f in flist:
        fin = csv.reader(open(f + '/profiles.csv', 'r'))
        addDict = prof.builddict(fin)
        uin = csv.reader(open(f + '/users.csv', 'r'))
        uDict = user.builddict(uin)
        addR = bcr.buildRosterDict(addDict, uDict, locD)
        for i in iter(addR):
            if i not in fullR:
                fullR[i] = addR[i]
    
    outname = relLoc + 'FullRoster.csv'
    bcr.writeRoster(fullR, outname)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        locname = sys.argv[1]
    else:
        locname = utils.getFileName('Enter name of the id=>location file :')
   
    main(locname)
