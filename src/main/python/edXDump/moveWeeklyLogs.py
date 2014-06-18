#!/usr/bin/env python
"""
Move the weekly logs created by separateClassLogs to the directory for the course,
and rename the log WeekLog. This program should be run from a directory one above
those that contain the the class log files (i.e., the program should be run from 
a directory that contains prod directories, each of which has the class logs in 
them). 
Created on Feb 23, 2014

@author: waldo
"""
import sys
import shutil
import glob
import os

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: moveWeeklyLogs srcDir destDir'
        exit()
        
    srcDir = sys.argv[1]
    destDir = sys.argv[2]
    
    fileList = glob.glob(srcDir + '/*.log')
    for fname in fileList:
        if 'unknown' not in fname:
            cname = fname[:fname.find('.log')]
            if not os.path.isdir(destDir + '/' + cname):
                os.mkdir(destDir + '/' + cname)
            destFile = destDir + '/' + cname + '/WeekLog'
            try:
                shutil.move(fname, destFile)
            except:
                print 'unable to move file', fname, 'to', destFile