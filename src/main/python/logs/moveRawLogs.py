'''
Created on Feb 23, 2014

@author: waldo
'''
import shutil
import glob
import sys

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'Usage: moveRawLogs destdir'
        exit()
    destDir = sys.argv[0]
    flist = glob.glob('*/*/2014*.log')
    for f in flist:
        destf = destDir + '/' + f
        shutil.move(f, destf)