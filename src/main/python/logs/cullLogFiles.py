#!/usr/bin/env python
'''
Find and delete all of the log files before a given date

This script, when run from a directory that contains a set of log files with names following
the pattern
    YYYY-MM-DD-*
will delete all of the files dated prior to the supplied date (also given in the form
YYYY-MM-DD ). This is useful to only build on log files that are new. If the script is
called with no supplied date, it will simply exit.

'''
import os
import sys

fileList = os.listdir(os.getcwd())
if len(sys.argv) > 1:
    cmpDate = sys.argv[1]
else:
    exit()

for f in fileList:
    if f <= cmpDate:
        os.remove(f)
