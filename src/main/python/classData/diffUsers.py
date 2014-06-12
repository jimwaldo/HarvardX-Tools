#!/usr/bin/env python
'''
Examine a set of users.csv files for a class over some weeks, finding any differences

This program is meant to be run from a directory of weekly dumps from edX. It
finds all sub-directories and then looks for the class number supplied as a 
command-line argument. It goes into those class directories, and compares the
users.csv files in those directories, creating a .csv file with the user id and
user name for any user who is in one week and not in the next, or not in the first
week and then in the next.

    Command line arguments
    ======================
    The name of a class (assumed to be the name of a sub-directory of the current 
    directory) that is to have the user lists compared
    
'''

import glob
import sys
import csv
import classData.user as user

course = sys.argv[1]
flist = glob.glob('harvardx*/' + course + '/users.csv')
if len(flist) < 2:
    exit()

f = iter(flist).next()
flist.remove(f)
ufile = open(f, 'r')
oldDict = user.builddict(ufile)
ufile.close()
out = csv.writer(open(course+'diffs.csv', 'w'))
for f in flist:
    ufile = open(f, 'r')
    newDict = user.builddict(csv.reader(ufile))
    ufile.close()
    out.writerow(['In older course list, not new'])
    i = 0
    for u in iter(oldDict):
        if u not in newDict:
            out.writerow([u, oldDict[u].username])
            i += 1
    out.writerow(['Total deleted between files: ', str(i)])
    i = 0
    out.writerow(['In new course list, not old'])
    for u in iter(newDict):
        if u not in oldDict:
            out.writerow([u, newDict[u].username])
            i += 1
    out.writerow(['Total added between files : ', str(i)])
    oldDict = newDict


        
