#!/usr/bin/env python
'''
Created on Jul 1, 2014

@author: waldo




'''
import glob
import sys
import csv

def addEvent(hdict, clDate, nev):
    if (clDate in hdict):
        hdict[clDate] += nev
    else:
        hdict[clDate] = nev
    return
        
def buildFromFile(fin, clDate, cdict):
    for cname, nev in fin:
        if cname not in cdict:
            cdict[cname] = {}
        addEvent(cdict[cname], clDate, nev)
    return
  
def getDatefromName(fname):
    return (fname[9:19])    
      
def processWeek(clDict, f):
    print "processing file", f
    ff = open(f, 'r')
    fin = csv.reader(ff)
    fDate = getDatefromName(f)
    buildFromFile(fin, fDate, clDict)
    ff.close()      
    return
      
def writeHistFile(c, histDict):
    fname = c + 'EvHist.csv'
    f = open(fname, 'w')
    fout = csv.writer(f)
    fout.writerow(['Date','Event Count'])
    for d in sorted(histDict.iterkeys()):
        fout.writerow([d, histDict[d]])
    f.close()
    return

if __name__ == '__main__':
    flist = glob.glob('*/*/ClassList.csv')
    if not flist:
        print 'No files found'
        sys.exit(1)
    clDict = {}
    for f in flist:
        processWeek(clDict, f)
        
    for c in clDict.keys():
        writeHistFile(c, clDict[c])