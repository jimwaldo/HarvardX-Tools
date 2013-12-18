#!/usr/bin/env python
'''
Created on Dec 13, 2013

@author: waldo
'''
import json
import glob
import csv
import sys

def readFromLog(toDict,fromFile):
    #dc = json.JSONDecoder()
    for line in fromFile:
        try:
            dcl = json.loads(line)
            cl = dcl['context']['course_id']
            if cl in toDict:
                toDict[cl] += 1
            else:
                toDict[cl] = 1
        except ValueError:
            pass
    return toDict
    
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        d = sys.argv[1]
    else:
        d = ''
    flist = glob.glob(d + '/' + '*.log')
    cDict = {}
    for f in flist:
        fin = open(f, 'r')
        cDict = readFromLog(cDict, fin)
        fin.close()
        
    fout = csv.writer(open('ClassList.csv', 'w'))
    fout.writerow(['Classname', 'Count'])
    for v in iter(cDict):
        fout.writerow([v, cDict[v]])