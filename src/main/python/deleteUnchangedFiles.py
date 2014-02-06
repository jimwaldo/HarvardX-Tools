#!/usr/bin/env python

'''
Created on Dec 24, 2013

@author: waldo
'''
import filecmp
import glob
import os
import sys


if __name__ == '__main__':
    print len(sys.argv)
    if len(sys.argv) == 2:
        cmpDir = sys.argv[1]
    else:
        print 'Usage: deleteUnchangedFile destDir'
        sys.exit(1)
    
    allFiles = glob.glob('*/*/*')
    unchangedListf = open('UnchangedFileList', 'w')
    unchangedListf.write(cmpDir+'\n')
    for f in allFiles:
        f2 = cmpDir + '/' + f
        if os.path.exists(f2):
            if filecmp.cmp(f, f2):
                unchangedListf.write(f + '\n')
                #os.remove(f2)
    unchangedListf.close()
            