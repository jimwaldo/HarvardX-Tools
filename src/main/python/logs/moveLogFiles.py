#!/usr/bin/env python
'''
Move a set of log files to the directory of the class with which they are associated.

This is a brute-force script, that keeps a hand-maintained list of log-file to class
names. The script takes as arguments a source file directory and a destination file
directory; the source file should be a directory where the logs named as the key to 
the dictionary are found, and the destination should be the name of a directory 
containing the class directories named as the value of each of the dictionary
entries. The log files will be moved to that directory, and renamed 'WeekLog'

Created on Dec 3, 2013

@author: waldo
'''

import os
import sys

nameMap = {
           'AI12.1xprod.log' : 'AI12.1x-2013_SOND',
           'AI12.2xprod.log' : 'AI12.2x-2013_SOND',
           'CB22x.1xprod.log' : 'CB22.1x-2013_SOND',
           'CB22.1xprod.log' : 'CB22.1x-2013_SOND',
           'CB22xedge.log' : 'CB22.1x-2013_SOND-edge',
           'CB22xprod.log' : 'CB22x-2013_Spring',
           'ER22xprod.log' : 'ER22x-2013_Spring',
           'CS50prod.log' : 'CS50-2012H',
           'CS50x-2012prod.log' : 'CS50x-2012',
           'CS50x-2014prod.log' : 'CS50x-2014_T1',
           'GSE1xprod.log' : 'GSE1x-2014_JFMA',
           'HDS1544edge.log' : 'HDS1544.1x-3T2013-edge',
           'HDS1544prod.log' : 'HDS1544.1x-2013_SOND',
           'HKS211.1xedge.log' : 'HKS_211.1x-3T2013-edge',
           'HKS211.1xprod.log' : 'HKS211.1x-3T2013',
           'HLS1prod.log' : 'HLS1xA-Copyright',
           'HMS214xprod.log' : 'HSPH-HMS214x-2013_SOND',
           'MCB80.1xprod.log' : 'MCB80.1x-2013_SOND',
           'PH201xprod.log' : 'PH201x-2013_SOND',
           'PH201xedge.log' : 'PH201x-3T2013-edge',
           'PH207xprod.log' : 'PH207x-2012_Fall',
           'PH278xprod.log' : 'PH278x-2013_Spring',
           'SPU17xedge.log' : 'SPU17x-The_Einstein_Revolution-edge',
           'SPU27xprod.log' : 'SPU27x-2013_Oct',
           'SW12_Octedge.log' : 'SW12X-China-edge',
           'SW12_Octgedge.log' : 'SW12X-China-edge',
           'SW12_Octprod.log' : 'SW12x-2013_Oct',
           'SW12_SONDprod.log' : 'SW12x-2013_SOND',
           'SW-12edge.log' : 'SW-12X-2013_Fall-edge',
           }

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print "Usage: moveLogFiles.py fromDirectory ToDirectory"
        exit(0)
        
    fromDir = sys.argv[1]
    toDir = sys.argv[2]
#    print 'from directory = ', fromDir, ', to directory =', toDir
    
    for k in nameMap:
        fromFile = fromDir + '/' + k
        toFile = toDir + '/'+ nameMap[k] + '/WeekLog'
        #print 'About to move', fromFile, 'to', toFile
        if os.path.exists(fromFile) and os.path.exists(toDir + '/' + nameMap[k]):
            #print 'About to move', fromFile, 'to', toFile
            os.rename(fromFile, toFile)
        