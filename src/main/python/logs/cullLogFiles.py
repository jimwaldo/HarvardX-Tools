#!/usr/bin/env python
"""
Find and delete all of the log files before a given date

This script, when run from a directory that contains a set of log files with names following
the pattern
    YYYY-MM-DD-*
will delete all of the files dated prior to the first supplied date (also given in the form
YYYY-MM-DD ) and greater than or equal to the second supplied date. This is useful to only 
build on log files that are new, but allows excluding partial files. The first date supplied should be
the date of the last log file processed (generally during the previous week), and the second 
date should be the date of any partial files that should be excluded. 

If the script is called with no supplied date, it will simply exit after printing usage information.

This file is only needed until edX begins to supply incremental data updates (that is, only new
data). This is under discussion, but has been under discussion for most of a year, so this file
is still in use.

"""
import glob
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) > 2:
        startDate = sys.argv[1]
        endDate = sys.argv[2]
    else:
        print "Usage: cullLogFiles fromDate toDate, where"
        print "fromDate is the first date to be included and"
        print "toDate is the first date to be excluded"
        exit()
    fileList = glob.glob('20*')
    for f in fileList:
        fdate = f[:f.index('_')]
        if (fdate < startDate) or (fdate >= endDate):
            os.remove(f)

