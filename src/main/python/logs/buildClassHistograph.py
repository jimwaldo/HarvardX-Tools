#!/usr/bin/env python
"""
Run from a directory containing directories with name harvardx-YYYY-MM-DD and which has
a set of directories that might contain a ClassList.csv file, this program will 
create a set of csv files (written to the current directory) that will contain a line
for each date (as determined by the directory name) and the count of the events during
the week ending with that date. 

@author: waldo




"""
import glob
import sys
import csv
import re

def addEvent(hdict, clDate, nev):
    """
    Add a count of events to the supplied dictionary for a class, 
    for the date supplied. If there is already an entry for this 
    date, it means that the course is being offered in multiple forms
    (i.e., both edge and on-line) and the additional events should be
    added to the total
    TODO: when doing incremental updates, there needs to be some
    way of determining if the count should be added (if the course if
    being offered in multiple cases) or ignored (if it is the second time
    the events for this week have been attempted to add)
    """
    if (clDate in hdict):
        hdict[clDate] += nev
    else:
        hdict[clDate] = nev
    return
        
def buildFromFile(fin, clDate, cdict):
    """
    Read in a csv file with lines of classname, number of events and 
    add the events to the dictionary for the class. If the class does
    not have an event dictionary, create one for it. 
    """
    for cname, nev in fin:
        if cname not in cdict:
            cdict[cname] = {}
        addEvent(cdict[cname], clDate, nev)
    return
  
def getDatefromName(fname):
    """
    Returns the date of the form YYYY-MM-DD from fname, or an empty
    string if there is no string that matches. If there are multiple
    matches, this returns the first of them.
    """
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", fname)
    if len(dates) == 0:
        return ''
    else:
        return(dates[1])
    
def getClassfromFileName(fname):
    """
    Get a class name from the filename. Assume that the filename 
    is formed from the classname + EvHist.csv, strip any directory
    names and then return the class preface in what is left.
    """
    if '/' in fname:
        fileName = fname[fname.rindex('/')+1:]
    else:
        fileName = fname
    return fileName[ : fileName.rindex('EvHist')]
    
def getFileNamefromClass(cName, dirName=''):
    """
    Construct a filename from the class name. Buy default, the
    file will be in the current working directory. A directory name
    can be passed in as well; if it is it is prepended to the 
    filename
    """
    fname = cName + 'EvHist.csv'
    if len(dirName) != 0:
        fname = dirName + '/' + fname
    return fname
         
      
def processWeek(clDict, f):
    """
    Given a file name and a dictionary of events indexed by class names,
    open the file, make a csv.reader object, process the file, and then
    close the open file. 
    """
    print "processing file", f
    ff = open(f, 'r')
    fin = csv.reader(ff)
    fDate = getDatefromName(f)
    buildFromFile(fin, fDate, clDict)
    ff.close()      
    return
      
def writeHistFile(c, histDict):
    """
    Writes a file of week, event count for a particular class. The file
    will be named by the class name + EvHist.csv.
    """
    fname = getFileNamefromClass(c)
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
