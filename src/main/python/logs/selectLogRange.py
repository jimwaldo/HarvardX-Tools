#!/usr/bin/env python

'''
Created on Dec 22, 2013

@author: waldo
'''

import shutil
import sys
import glob

def getFiles(srcDir, fromDate, toDate):
    retList = []
    candidates = glob.glob(srcDir + '/*/*.log')
    for f in candidates:
        fname = f[f.rfind('/')+1:]
        fdate = fname[:fname.find('_')]
        if (fromDate <= fdate) and (fdate <= toDate):
            retList.append(f)
    return retList

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage: selectLogRange srcDir destDir fromDate [toDate]"
        sys.exit(1)
        
    srcDir = sys.argv[1]
    print srcDir
    destDir = sys.argv[2]
    print destDir
    fromDate = sys.argv[3]
    print fromDate
    if len(sys.argv) > 4:
        toDate = sys.argv[4]
    else:
        toDate = '2020'
    print toDate
    copyList = getFiles(srcDir, fromDate, toDate)
    print copyList
    
        
    
