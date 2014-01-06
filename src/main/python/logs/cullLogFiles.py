#!/usr/bin/env python
'''
Find and delete all of the log files before a given date

This script, when run from a directory that contains a set of log files with names following
the pattern
    YYYY-MM-DD-*
will delete all of the files dated prior to or equal to the supplied date (also given in the form
YYYY-MM-DD ). This is useful to only build on log files that are new. The date supplied should be
the date of the last log file processed (generally during the previous week). 

If the script is called with no supplied date, it will simply exit.

'''
import glob
import os
import sys

fileList = glob.glob('20*')
if len(sys.argv) > 1:
    cmpDate = sys.argv[1]
else:
    exit()

for f in fileList:
    fdate = f[:f.index('_')]
    if fdate <= cmpDate:
        os.remove(f)
