#!/usr/bin/env python
"""
Created on Feb 23, 2014

Move the raw log files from their position under the various weekly directories to 
a full directory of all of the raw log files. This is run to get the raw logs in the
right place for the scripts that add them to the mongodb to process.
"""
import shutil
import glob
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: moveRawLogs destdir'
        exit()
    destDir = sys.argv[1]
    flist = glob.glob('*/*/20*/20*.log') # Assume new dir structure HarvardX/courses.edx.org/YYYY/YYYY-MM-DD.log
    for f in flist:
        #print f
        destf = destDir + '/' + f
        shutil.move(f, destf)
