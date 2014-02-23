#!/usr/bin/env python
'''
Move the weekly logs created by separateClassLogs to the directory for the course,
and rename the log WeekLog. 
Created on Feb 23, 2014

@author: waldo
'''
import sys
import shutil
import glob

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: moveWeeklyLogs srcDir destDir'
        exit()
        
    srcDir = sys.argv[0]
    destDir = sys.argv[1]
    
    fileList = glob.glob(srcDir + '/*.log')
    for fname in fileList:
        cname = fname[:fname.find('.log')]
        destFile = destDir + '/' + cname + '/WeekLog'
        shutil.move(fname, destFile)